from Board.BoardView import BoardView
from Player.PlayerView import PlayerView
from ViewObject import ViewObject
from functions import can_call


class GameView(ViewObject):
    def __init__(self, app):
        super().__init__(None, app, 0, 0)
        w, h = app.screen.get_width(), app.screen.get_height()
        self.set_children([
            *(PlayerView(player, app, w, h) for player in app.players()),
            BoardView(app.board(), app, w, h),
            app.cursor.view()
        ])
        self.focused_object = self.get_focused_object()

    def get_focused_object(self):
        touched_object = self.check_focus()
        if touched_object is None:
            return

        if can_call(touched_object, 'on_focus'):
            touched_object = touched_object.on_focus()
        touched_object.focused = True
        return touched_object

    def draw(self, screen):
        screen.fill((64, 180, 64))
