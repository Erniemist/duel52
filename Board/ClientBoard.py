from Board.Board import Board
from Board.Lane.ClientLane import ClientLane


class ClientBoard(Board):
    def __init__(self, game, players, lane_data):
        super().__init__(game, [
            ClientLane.from_json(game=game, players=players, lane_id=i, data=lane_data)
            for i, lane_data in enumerate(lane_data)
        ])

    @staticmethod
    def from_json(game, players, data):
        return ClientBoard(game=game, players=players, lane_data=data['lanes'])
