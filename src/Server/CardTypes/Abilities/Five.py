from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Effects.Effect import Effect


class Five(OnFlip):
    description = 'When this card flips, flip all friendly minions in the same lane.'

    def __init__(self, card, game, trigger):
        self.card = card
        super().__init__(parts=[
            Effect(self.flip_friendly_in_lane)
        ])

    def flip_friendly_in_lane(self):
        for card in self.card.host.cards:
            card.minion.flip_up()
