from Client.Board.BoardView import BoardView
from Client.Board.Lane.Side.Minion.ClientMinion import ClientMinion
from Client.Card.CardDescription import CardDescription
from Client.Card.ClientCard import ClientCard
from Client.Cursor.Target import Target
from Client.Cursor.TargetView import TargetView
from Client.Player.PlayerView import PlayerView
from Client.Text import Text
from Client.ViewObject import ViewObject
from functions import can_call


class GameView(ViewObject):
    def __init__(self, app):
        super().__init__(None, app, 0, 0)
        w, h = app.screen.get_width(), app.screen.get_height()
        children = [
            *(PlayerView(player, app, w, h) for player in app.players()),
            BoardView(app.board(), app, w, h),
            app.cursor.view(),
        ]
        if self.app.game_state.pending_attack:
            attack = self.app.game_state.pending_attack
            children.append(TargetView(attack.attacker, Target.RED, self.app, attack.targets[0].view_object.get_centre()))
        if self.app.game_state.winner is not None:
            if self.app.game_state.winner == self.app.team:
                children.append(Text(self.app, 'You won!', w / 2, h / 2, 100))
            else:
                children.append(Text(self.app, 'You lost', w / 2, h / 2, 100))
        card = self.show_card_description()
        if card:
            children.append(CardDescription(self.app, card, w))
        self.set_children(children)
        self.focused_object = self.get_focused_object()

    def show_card_description(self):
        view_object = self.app.focused_object()
        if not view_object:
            return None
        focused = view_object.real
        if focused is None:
            return None
        card = None
        if isinstance(focused, ClientCard):
            card = focused
        if isinstance(focused, ClientMinion):
            card = focused.card
        if not card:
            return None
        if card.card_id not in self.app.my_player().known_cards:
            return None
        return card

    def get_focused_object(self):
        if self.app.game_state.winner is not None:
            return
        touched_object = self.check_focus()
        if touched_object is None:
            return

        if can_call(touched_object, 'on_focus'):
            touched_object = touched_object.on_focus()
        touched_object.focused = True
        return touched_object

    def draw(self, screen):
        screen.fill((64, 180, 64))
