from Board.BoardView import BoardView
from Player.PlayerView import PlayerView
from ViewObject import ViewObject


class GameView(ViewObject):
    def __init__(self, game):
        super().__init__(game, game, 0, 0)
        w, h = game.screen.get_width(), game.screen.get_height()
        self.set_children([
            *(PlayerView(player, game, w, h) for player in game.players()),
            BoardView(game.board(), game, w, h),
            game.cursor.view(game)
        ])
