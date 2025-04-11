from Client.Board.Lane.Side.Minion.Minion import Minion
from Client.Cursor.Target import Target
from Server.CardTypes.Abilities.Stealth import Stealth


class ClientMinion(Minion):
    def __init__(self, card, game, minion_data):
        self.card = card
        self.game = game
        self.value = card.value
        self.player = self.side.player
        self.team = self.player.team
        self.max_hp = minion_data.max_hp
        self.hp = minion_data.hp
        self.face_down = minion_data.face_down
        self.attacks_made = minion_data.attacks_made
        self.max_attacks = minion_data.max_attacks
        self.frozen = minion_data.frozen
        self.pair = None
        self.view_object = None

    @property
    def side(self):
        return self.card.host

    def can_select(self, my_turn):
        if self.frozen:
            return False
        if not my_turn or self.team != self.game.active_player().team or self.player.actions < 1:
            return False
        return not self.pair or self.attacks_left() > 0

    def on_select(self, cursor):
        if self.face_down:
            self.game.flip_action(self)
        else:
            cursor.set_target_source(Target.harm(source=self))

    def can_hover(self, player):
        return self.card.card_id in player.known_cards

    def on_hover(self):
        pass

    def can_choose(self, choice):
        return choice.could_choose(self.card)

    def on_choose(self):
        self.game.submit_choice(self.card.card_id)

    def can_target(self, target_source, my_turn):
        if self.game.active_player().team != self.team:
            return self.can_be_attacked(target_source)
        return my_turn and self.can_pair(target_source)

    def can_be_attacked(self, target_source):
        if target_source.side.lane != self.side.lane:
            return False
        if target_source.attacks_left() < 1:
            return False
        if self.has_active_keyword(Stealth) and self.game.pending_attack:
            return False
        return True

    def can_pair(self, target_source):
        if self.face_down:
            return False
        if self.pair or target_source.pair:
            return False
        return self.value == target_source.value

    def on_target(self, target_source):
        if self.game.active_player().team != self.team:
            self.game.attack(target_source, self)
        else:
            self.game.pair_action(target_source, self)

    def has_active_keyword(self, keyword):
        return not self.face_down and self.card.has_keyword(keyword)
