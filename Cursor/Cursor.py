from Cursor.CursorCardView import CursorCardView
from Cursor.TargetView import TargetView
from ViewObject import ViewObject


class Cursor:
    def __init__(self, game):
        self.game = game
        self.position = (0, 0)
        self.offset = (0, 0)
        self.card = None
        self.target_source = None

    def view(self, game):
        if self.card:
            return CursorCardView(self.card, game, self.card_position())
        if self.target_source:
            return TargetView(self, game, self.start_pos(), self.position)
        return ViewObject(self, game, 0, 0)

    def start_pos(self):
        return self.target_source.view_object.get_centre()

    def add_card(self, card):
        if self.card:
            raise Exception('Cursor has card')
        self.card = card

    def set_offset(self, card_view):
        x, y = self.position
        c_x, c_y = card_view.position()
        self.offset = (c_x - x, c_y - y)

    def remove_card(self, card):
        if not self.card:
            raise Exception('No card to put down')
        self.card = None

    def card_position(self):
        o_x, o_y = self.offset
        x, y = self.position
        return x + o_x, y + o_y

    def set_target_source(self, minion):
        self.target_source = minion

    def cancel(self):
        match self.mode():
            case 'target':
                self.target_source = None
            case 'place':
                self.card = None

    def cancel_target(self):
        self.target_source = None

    def mode(self):
        if self.card:
            return 'place'
        elif self.target_source:
            return 'target'
        else:
            return 'select'

    def click_method_name(self):
        return 'on_' + self.mode()

    def validation_method_name(self):
        return 'can_' + self.mode()

    def click_method(self):
        mode = self.mode()
        if mode == 'place':
            return lambda x: x.on_place(self.game, self.card)
        if mode == 'target':
            return lambda x: x.on_target(self.game, self.target_source)
        else:
            return lambda x: x.on_select(self.game)

    def validation_method(self):
        mode = self.mode()
        if mode == 'place':
            return lambda x: x.can_place(self.game, self.card)
        if mode == 'target':
            return lambda x: x.can_target(self.game, self.target_source)
        else:
            return lambda x: x.can_select(self.game)
