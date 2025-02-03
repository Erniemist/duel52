from typing import Generator, Any
from Client.Card.ClientCard import ClientCard
from Client.Board.Lane.ClientLane import ClientLane


class ClientBoard:
    def __init__(self, game, players, lane_data):
        self.game = game
        self.lanes = [
            ClientLane.from_json(game=game, players=players, lane_id=i, data=lane_data)
            for i, lane_data in enumerate(lane_data)
        ]

    def get_cards(self) -> Generator[ClientCard, Any, None]:
        return (card for lane in self.lanes for card in lane.get_cards())

    @staticmethod
    def from_json(game, players, data):
        return ClientBoard(game=game, players=players, lane_data=data['lanes'])
