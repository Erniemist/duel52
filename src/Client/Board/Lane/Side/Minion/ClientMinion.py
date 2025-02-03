from Client.Board.Lane.Side.Minion.Minion import Minion


class ClientMinion(Minion):
    def __init__(self, card, side, game, hp, face_down, attacks_made, pair_id):
        self.card = card
        self.value = card.value
        self.side = side
        self.player = side.player
        self.team = self.player.team
        self.game = game
        self.hp = hp
        self.face_down = face_down
        self.attacks_made = attacks_made
        self.pair = None
        self.view_object = None
        if pair_id is None:
            return
        other = next((card for card in self.side.cards if card.card_id == pair_id), None)
        if other is None:
            return
        self.pair_with(other.minion)

    def can_select(self, my_turn):
        if not my_turn or self.team != self.game.active_player().team or self.player.actions < 1:
            return False
        return not self.pair or self.attacks_left() > 0

    def on_select(self, cursor):
        if self.face_down:
            self.game.flip_event(self)
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
            self.game.attack_event(target_source, self)
        else:
            self.game.pair_event(target_source, self)

    @staticmethod
    def from_json(card, side, game, data):
        pair = None
        if 'pair' in data.keys():
            pair = data['pair']
        return ClientMinion(
            card=card,
            side=side,
            game=game,
            hp=data['hp'],
            face_down=data['face_down'],
            attacks_made=data['attacks_made'],
            pair_id=pair,
        )
