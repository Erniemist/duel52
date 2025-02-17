from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Effects.Effect import Effect


class Six(OnFlip):
    description = 'When this card flips, freeze all enemy minions in the same lane.'

    def __init__(self, card, game, trigger):
        self.card = card
        super().__init__(parts=[
            Effect(lambda: self.freeze_all_enemy_in_lane())
        ])

    def freeze_all_enemy_in_lane(self):
        for other_card in self.card.host.other_side().cards:
            other_card.minion.frozen = True
