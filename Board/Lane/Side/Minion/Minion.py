class Minion:
    max_hp = 2
    max_attacks = 1

    def __init__(self, card, side, game, hp, face_down, attacks_made):
        self.card = card
        self.value = card.value
        self.side = side
        self.player = side.player
        self.team = self.player.team
        self.game = game
        self.hp = hp
        self.face_down = face_down
        self.pair = None
        self.attacks_made = attacks_made

    def attacks_left(self):
        return self.max_attacks - (self.attacks_made + (self.pair.attacks_made if self.pair else 0))

    def pair_with(self, other):
        self.pair = other
        other.pair = self

    def could_pair(self):
        return self.pair is None and self.value in [
            other.value
            for other in self.side.cards
            if other.minion is not self and other.minion.pair is None
        ]

    def could_attack(self):
        return self.attacks_left() > 0 and len([
            enemy
            for enemy in self.player.other_player().minions()
            if enemy.side == self.side
        ]) > 0

    def could_act(self):
        return self.could_attack() or self.face_down or self.could_pair()
