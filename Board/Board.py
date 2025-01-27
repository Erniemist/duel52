import json

from Board.Lane.Lane import Lane


class Board:
    num_lanes = 3

    def __init__(self, game):
        self.game = game
        self.lanes = [Lane(game) for i in range(self.num_lanes)]

    def to_json(self):
        return {
            'lanes': [lane.to_json() for lane in self.lanes]
        }

    @staticmethod
    def from_json(game, data):
        board = Board(game=game)
        board.lanes = [Lane.from_json(game=game, data=lane_data) for lane_data in data['lanes']]
        return board
