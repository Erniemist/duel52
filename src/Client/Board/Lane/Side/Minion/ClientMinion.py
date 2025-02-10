from Client.Board.Lane.Side.Minion.Minion import Minion


class ClientMinion(Minion):
    def __init__(self, card, side, game, minion_data):
        self.card = card
        self.side = side
        self.game = game
        self.value = card.value
        self.player = side.player
        self.team = self.player.team
        self.hp = minion_data.hp
        self.face_down = minion_data.face_down
        self.attacks_made = minion_data.attacks_made
        self.frozen = minion_data.frozen
        self.pair = None
        self.view_object = None

    def can_select(self, my_turn, awaiting_choice):
        if awaiting_choice:
            return awaiting_choice.could_choose_minion(self)
        if self.frozen:
            return False
        if not my_turn or self.team != self.game.active_player().team or self.player.actions < 1:
            return False
        return not self.pair or self.attacks_left() > 0

    def on_select(self, cursor, awaiting_choice):
        if awaiting_choice:
            self.game.submit_choice(self.card.card_id)
        if self.face_down:
            self.game.flip_action(self)
        else:
            cursor.set_target_source(self)

    def can_target(self, target_source, my_turn):
        if self.game.active_player().team != self.team:
            return self.can_be_attacked(target_source)
        return my_turn and self.can_pair(target_source)

    def can_be_attacked(self, target_source):
        if target_source.attacks_left() < 1:
            return False
        return target_source.side.lane == self.side.lane

    def can_pair(self, target_source):
        if self.face_down:
            return False
        if self.pair or target_source.pair:
            return False
        return self.value == target_source.value

    def on_target(self, target_source):
        if self.game.active_player().team != self.team:
            self.game.attack_action(target_source, self)
        else:
            self.game.pair_action(target_source, self)
