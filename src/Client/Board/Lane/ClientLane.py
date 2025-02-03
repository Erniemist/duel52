from typing import Generator, Any
from Client.Board.Lane.Side.ClientSide import ClientSide
from Client.Card.ClientCard import ClientCard


class ClientLane:
    def __init__(self, game, players, lane_id, sides_data):
        self.game = game
        self.players = players
        self.lane_id = lane_id
        self.sides = [
            ClientSide.from_json(lane=self, side_id=lane_id * 2 + i, player=player, game=game, data=side_data)
            for i, player, side_data in zip(range(len(sides_data)), players, sides_data)
        ]

    def get_cards(self) -> Generator[ClientCard, Any, None]:
        return (card for side in self.sides for card in side.cards)

    @staticmethod
    def from_json(game, players, lane_id, data):
        return ClientLane(game=game, players=players, lane_id=lane_id, sides_data=data['sides'])
