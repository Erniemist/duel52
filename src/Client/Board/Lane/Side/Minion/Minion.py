from typing import Self


class Minion:
    max_hp = 2
    max_attacks: int
    attacks_made: int
    pair: None | Self

    def attacks_left(self):
        return self.max_attacks - (self.attacks_made + (self.pair.attacks_made if self.pair else 0))

    def pair_with(self, other):
        self.pair = other
        other.pair = self

