from Board.Lane.Side.Minion.MinionView import MinionView
from ViewObject import ViewObject


class PairView(ViewObject):
    def __init__(self, first, second, game, position):
        self.team = first.team
        super().__init__(first, game, *position)
        offset = MinionView.w / 5
        self.first_view = MinionView(first, game, (0, 0))
        self.second_view = MinionView(second, game, (offset, offset))
        self.set_children([self.first_view, self.second_view])

    def check_focus(self, mouse):
        second_focus = self.second_view.check_focus(mouse)
        first_focus = self.first_view.check_focus(mouse)
        if self.game.cursor.mode() == 'target' and self.game.cursor.target_source.team != self.team:
            return second_focus if second_focus is not None else first_focus
        return self if (second_focus is not None or first_focus is not None) else None

    def on_focus(self):
        self.first_view.focused = True
        self.second_view.focused = True
        return self
