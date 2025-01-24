from Board.BoardView import BoardView
from Board.Lane.Lane import Lane


class Board:
    num_lanes = 3

    def __init__(self, game):
        self.game = game
        self.lanes = [Lane(game) for i in range(self.num_lanes)]

    def view(self):
        return BoardView(self, self.game.screen.get_width(), self.game.screen.get_height())
