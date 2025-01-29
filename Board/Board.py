from Board.Lane.Lane import Lane


class Board:
    num_lanes = 3

    def __init__(self, game):
        self.game = game
        self.lanes = [Lane(game, lane_id=i) for i in range(self.num_lanes)]

    def to_json(self, player):
        return {'lanes': [lane.to_json(player) for lane in self.lanes]}

    @staticmethod
    def from_json(game, data):
        board = Board(game=game)
        board.lanes = [
            Lane.from_json(game=game, lane_id=i, data=lane_data)
            for i, lane_data in enumerate(data['lanes'])
        ]
        return board
