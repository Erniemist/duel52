from Board.Lane.Lane import Lane
from Board.Lane.Side.Side import Side


class ClientLane(Lane):
    def __init__(self, game, players, lane_id, sides_data):
        super().__init__(game, players, lane_id, [
            Side.from_json(lane=self, side_id=lane_id * 2 + i, player=player, game=game, data=side_data)
            for i, player, side_data in zip(range(len(sides_data)), players, sides_data)
        ])

    @staticmethod
    def from_json(game, players, lane_id, data):
        return ClientLane(game=game, players=players, lane_id=lane_id, sides_data=data['sides'])
