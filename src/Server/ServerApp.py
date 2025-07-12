import json
import uuid

from websockets import ServerConnection

from DataTransfer.ChoiceData import ChoiceData
from DataTransfer.GameData import GameData
from Server.Actions.FlipAction import FlipAction
from Server.Actions.PlayAction import PlayAction
from Server.Actions.AttackAction import AttackAction
from Server.Actions.PairAction import PairAction
from Server.ServerGameState import ServerGameState
from Server.ServerPlayer import ServerPlayer


class ServerApp:
    def __init__(self, name: str, game):
        self.name = name
        self.game_id = str(uuid.uuid4().int)
        self.game: ServerGameState = game
        self.teams: dict[ServerConnection, str] = {}

    def add_connection(self, connection: ServerConnection, team: str):
        self.teams[connection] = team

    async def send(self, sender: ServerConnection, action_id: None | str = None):
        for connection, team in self.teams.items():
            data = {'game': GameData.from_server(self.game, team).to_json(), 'team': team}
            if connection == sender and action_id is not None:
                data['action_id'] = action_id
            if self.game.awaiting_choice() and team == self.game.awaited_choices[0].chooser.team:
                choice = self.game.awaited_choices[0]
                data['awaiting_choice'] = ChoiceData.from_server(self.game, choice).to_json()
            await connection.send(json.dumps(data))

    async def create(self, websocket: ServerConnection):
        team = ServerPlayer.TEAMS[0]
        self.add_connection(websocket, team)
        await self.send(websocket)

    async def join(self, websocket: ServerConnection):
        team = ServerPlayer.TEAMS[1]
        self.add_connection(websocket, team)
        await self.send(websocket)

    async def handle_action(self, websocket: ServerConnection, data: dict):
        print('team', self.teams[websocket])
        print(data)
        self.resolve_action(data, self.teams[websocket])
        await self.send(websocket, data['action_id'])

    def resolve_action(self, action_data, team):
        if self.expected_player().team != team:
            raise Exception(f'Non-active player attempted to take action: {action_data}')

        if self.game.awaiting_choice():
            if action_data['action'] != 'choose':
                raise Exception(f"Expected action to be 'choose', got {action_data['action']}")
            self.game.choose(action_data['data']['card'])
            return

        match action_data:
            case {'action': PlayAction.name, 'data': {'card': card_id, 'side': side_id}}:
                self.game.play(card_id, side_id)

            case {'action': FlipAction.name, 'data': {'card': card_id}}:
                self.game.flip(card_id)

            case {'action': PairAction.name, 'data': {'card_1': card_1_id, 'card_2': card_2_id}}:
                self.game.pair(card_1_id, card_2_id)

            case {'action': AttackAction.name, 'data': {'attacker': attacker, 'targets': targets}}:
                self.game.attack(attacker, targets)

            case _:
                raise Exception(f"Didn't recognise action: {action_data}")

    def expected_player(self):
        if not self.game.awaiting_choice():
            return self.game.active_player()
        return self.game.awaited_choices[0].chooser
