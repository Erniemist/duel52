from Board.Lane.Side.Minion.MinionView import MinionView
from ViewObject import ViewObject


class PairView(ViewObject):
    def __init__(self, first, second, position):
        self.team = first.team
        super().__init__(first, *position)
        offset = MinionView.w / 5
        self.first_view = MinionView(first, (0, 0))
        self.second_view = MinionView(second, (offset, offset))
        self.set_children([self.first_view, self.second_view])

    def check_focus(self, game, mouse):
        second_focus = self.second_view.check_focus(game, mouse)
        first_focus = self.first_view.check_focus(game, mouse)
        if game.cursor.mode() == 'target' and game.cursor.target_source.team != self.team:
            return second_focus if second_focus is not None else first_focus
        return self if (second_focus is not None or first_focus is not None) else None

    def on_focus(self):
        self.first_view.focused = True
        self.second_view.focused = True
        return self
