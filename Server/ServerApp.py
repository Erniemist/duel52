import json
import uuid

from Server.ServerGameState import ServerGameState
from Server.ServerPlayer import ServerPlayer


class ServerApp:
    def __init__(self, name):
        self.name = name
        self.game_id = str(uuid.uuid4().int)
        self.game = ServerGameState()
        self.teams = {}

    def add_connection(self, connection, team):
        connection.app = self
        self.teams[connection] = team

    def to_json(self, connection):
        return self.game.to_json(self.teams[connection])

    async def send(self, sender, event_id=None):
        for connection, team in self.teams.items():
            data = {'game': self.game.to_json(team), 'team': team}
            if connection == sender and event_id is not None:
                data['event_id'] = event_id
            await connection.send(json.dumps(data))

    async def create(self, websocket):
        team = ServerPlayer.TEAMS[0]
        self.add_connection(websocket, team)
        await self.send(websocket)

    async def join(self, websocket):
        team = ServerPlayer.TEAMS[1]
        self.add_connection(websocket, team)
        await self.send(websocket)

    async def handle_event(self, websocket, data):
        player = self.game.active_player()
        if player.team != self.teams[websocket]:
            raise Exception(f'Non-active player attempted to take action: {data}')
        match data:
            case {'event': 'play', 'data': {'side': side, 'card': card}}:
                side = self.game.find_side(side)
                card = self.game.find_card_from_hand(card)
                player.play_card(card=card, side=side)

            case {'event': 'flip', 'data': {'card': card}}:
                minion = self.game.find_card_from_board(card).minion
                player.flip_minion(minion)

            case {'event': 'pair', 'data': {'card_1': card_1, 'card_2': card_2}}:
                minion_1 = self.game.find_card_from_board(card_1).minion
                minion_2 = self.game.find_card_from_board(card_2).minion
                player.pair_minions(minion_1, minion_2)

            case {'event': 'attack', 'data': {'card_1': card_1, 'card_2': card_2}}:
                minion_1 = self.game.find_card_from_board(card_1).minion
                minion_2 = self.game.find_card_from_board(card_2).minion
                player.attack(minion_1, minion_2)

            case _:
                raise Exception(f"Didn't recognise event: {data}")

        await self.send(websocket, data['event_id'])
