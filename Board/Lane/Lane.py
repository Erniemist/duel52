import json

from Board.Lane.Side.Side import Side


class Lane:
    def __init__(self, game):
        self.game = game
        self.sides = [Side(game, self, player) for player in game.players]

    def to_json(self):
        return {
            'sides': [side.to_json() for side in self.sides]
        }

    @staticmethod
    def from_json(game, data):
        lane = Lane(game=game)
        lane.sides = [
            Side.from_json(lane=lane, player=player, game=game, data=side_data)
            for player, side_data in zip(game.players, data['sides'])
        ]
        return lane
