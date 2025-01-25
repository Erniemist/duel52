from Board.BoardView import BoardView
from Player.PlayerView import PlayerView
from ViewObject import ViewObject
from functions import can_call


class GameView(ViewObject):
    def __init__(self, game):
        super().__init__(game, game, 0, 0)
        w, h = game.screen.get_width(), game.screen.get_height()
        self.set_children([
            *(PlayerView(player, game, w, h) for player in game.players()),
            BoardView(game.board(), game, w, h),
            game.cursor.view(game)
        ])
        self.focused_object = self.get_focused_object()

    def get_focused_object(self):
        touched_object = self.check_focus(self.game.cursor.position)
        if touched_object is None:
            return

        if can_call(touched_object, 'on_focus'):
            touched_object = touched_object.on_focus()
        touched_object.focused = True
        return touched_object

    def draw(self, screen):
        screen.fill((64, 180, 64))
