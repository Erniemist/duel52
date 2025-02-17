from Client.Board.Lane.Side.Minion.MinionView import MinionView
from Client.ViewObject import ViewObject


class PairView(ViewObject):
    def __init__(self, first, second, app, position):
        self.team = first.team
        super().__init__(first, app, *position)
        offset = MinionView.w / 5
        self.first_view = MinionView(first, app, (0, 0))
        self.second_view = MinionView(second, app, (offset, offset))
        self.set_children([self.first_view, self.second_view])

    def check_focus(self):
        second_focus = self.second_view.check_focus()
        first_focus = self.first_view.check_focus()
        if self.app.cursor.mode() == 'target' and self.app.cursor.target_source().team != self.team:
            return second_focus if second_focus is not None else first_focus
        return self if (second_focus is not None or first_focus is not None) else None

    def on_focus(self):
        self.first_view.focused = True
        self.second_view.focused = True
        return self

    def get_centre(self):
        x1, y1 = self.first_view.get_centre()
        x2, y2 = self.second_view.get_centre()
        return (x1 + x2) / 2, (y1 + y2) / 2
