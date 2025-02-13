from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect


class Five(CardType):
    """When this card flips, flip all friendly minions in the same lane."""
    value = '5'

    class Ability(OnFlip):
        def __init__(self, card, game, trigger):
            self.card = card
            super().__init__(parts=[
                Effect(self.flip_friendly_in_lane)
            ])

        def flip_friendly_in_lane(self):
            for card in self.card.host.cards:
                card.minion.flip_up()

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability])
