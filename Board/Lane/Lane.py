import json

from Board.Lane.Side.Side import Side


class Lane:
    def __init__(self, game, lane_id):
        self.lane_id = lane_id
        self.game = game
        self.sides = [Side(game, self, side_id=lane_id * 2 + i, player=player) for i, player in enumerate(game.players)]

    def to_json(self):
        return {
            'sides': [side.to_json() for side in self.sides]
        }

    @staticmethod
    def from_json(game, lane_id, data):
        lane = Lane(game=game, lane_id=lane_id)
        lane.sides = [
            Side.from_json(lane=lane, side_id=lane_id * 2 + i, player=player, game=game, data=side_data)
            for i, player, side_data in zip(range(len(data['sides'])), game.players, data['sides'])
        ]
        return lane
