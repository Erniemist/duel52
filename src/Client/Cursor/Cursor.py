from Client.Board.Lane.Side.Minion.Minion import Minion
from Client.Card.ClientCard import ClientCard
from Client.Cursor.CursorCardView import CursorCardView
from Client.Cursor.TargetView import TargetView
from Client.ViewObject import ViewObject


class Cursor:
    def __init__(self, app):
        self.app = app
        self.position = (0, 0)
        self.offset = (0, 0)
        self.card_id = None
        self.target_source_id = None

    def card(self) -> ClientCard | None:
        if self.card_id is None:
            return None
        return self.app.find_card_from_hand(self.card_id)

    def target_source(self) -> Minion | None:
        if self.target_source_id is None:
            return None
        return self.app.find_card_from_board(self.target_source_id).minion

    def view(self):
        if self.card():
            return CursorCardView(self.card(), self.app, self.card_position())
        if self.target_source():
            return TargetView(self, self.app, self.start_pos(), self.position)
        return ViewObject(self, self.app, 0, 0)

    def start_pos(self):
        if self.target_source().pair:
            return self.target_source().view_object.parent.get_centre()
        return self.target_source().view_object.get_centre()

    def set_offset(self, card_view):
        x, y = self.position
        c_x, c_y = card_view.position()
        self.offset = (c_x - x, c_y - y)

    def card_position(self):
        o_x, o_y = self.offset
        x, y = self.position
        return x + o_x, y + o_y

    def set_target_source(self, minion):
        self.target_source_id = minion.card.card_id

    def cancel(self):
        match self.mode():
            case 'target':
                self.target_source_id = None
            case 'place':
                self.card_id = None

    def cancel_target(self):
        self.target_source_id = None

    def mode(self):
        if self.card():
            return 'place'
        elif self.target_source():
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
            return lambda x: self.place(x)
        if mode == 'target':
            return lambda x: self.target(x)
        else:
            return lambda x: x.on_select(self, self.app.awaiting_choice)

    def pick_up(self, card):
        self.card_id = card.card_id
        self.set_offset(self.app.game_view.focused_object)

    def place(self, game_object):
        game_object.on_place(self.card())
        self.card_id = None

    def target(self, game_object):
        game_object.on_target(self.target_source())
        self.cancel_target()

    def validation_method(self):
        mode = self.mode()
        if mode == 'place':
            return lambda x: x.can_place(self.card(), self.app.is_my_turn())
        if mode == 'target':
            return lambda x: x.can_target(self.target_source(), self.app.is_my_turn())
        else:
            return lambda x: x.can_select(self.app.is_my_turn(), self.app.awaiting_choice)
