import json
import uuid

from websockets import ServerConnection

from DataTransfer.GameData import GameData
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
        player = self.game.active_player()
        match action_data:
            case {'action': 'play', 'data': {'side': side, 'card': card}}:
                side = self.game.find_side(side)
                card = self.game.find_card_from_hand(card)
                player.play_card(card=card, side=side)

            case {'action': 'flip', 'data': {'card': card}}:
                minion = self.game.find_card_from_board(card).minion
                player.flip_minion(minion)

            case {'action': 'pair', 'data': {'card_1': card_1, 'card_2': card_2}}:
                minion_1 = self.game.find_card_from_board(card_1).minion
                minion_2 = self.game.find_card_from_board(card_2).minion
                player.pair_minions(minion_1, minion_2)

            case {'action': 'attack', 'data': {'card_1': card_1, 'card_2': card_2}}:
                minion_1 = self.game.find_card_from_board(card_1).minion
                minion_2 = self.game.find_card_from_board(card_2).minion
                player.attack(minion_1, minion_2)

            case _:
                raise Exception(f"Didn't recognise action: {action_data}")
        self.game.resolve_triggers()
