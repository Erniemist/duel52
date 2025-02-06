import json
import uuid

from websockets import ServerConnection

from DataTransfer.GameData import GameData
from Server.Actions.FlipAction import FlipAction
from Server.Actions.PlayAction import PlayAction
from Server.Actions.AttackAction import AttackAction
from Server.Actions.PairAction import PairAction
from Server.ServerGameState import ServerGameState
from Server.ServerPlayer import ServerPlayer


class Mode:
    EXPECTING_ACTION = 0
    EXPECTING_TARGET = 1
    def __init__(self, mode):
        self.mode = mode

    def am_expecting_action(self):
        return self.mode == self.EXPECTING_ACTION

    def am_expecting_target(self):
        return self.mode == self.EXPECTING_TARGET

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
        if self.game.active_player().team != self.teams[websocket]:
            raise Exception(f'Non-active player attempted to take action: {data}')
        self.resolve_action(data)
        await self.send(websocket, data['action_id'])

    def resolve_action(self, action_data):
        match action_data:
            case {'action': PlayAction.name, 'data': {'card': card_id, 'side': side_id}}:
                self.game.play(card_id, side_id)

            case {'action': FlipAction.name, 'data': {'card': card_id}}:
                self.game.flip(card_id)

            case {'action': PairAction.name, 'data': {'card_1': card_1_id, 'card_2': card_2_id}}:
                self.game.pair(card_1_id, card_2_id)

            case {'action': AttackAction.name, 'data': {'card_1': card_1_id, 'card_2': card_2_id}}:
                self.game.attack(card_1_id, card_2_id)

            case _:
                raise Exception(f"Didn't recognise action: {action_data}")
