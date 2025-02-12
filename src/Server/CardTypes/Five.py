from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect
from Server.Triggers.FlipTrigger import FlipTrigger


class Five(CardType):
    """When this card flips, flip all friendly minions in the same lane."""
    value = '5'

    class Ability1(Ability):
        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

        def __init__(self, card, game, player):
            self.card = card
            super().__init__(parts=[
                Effect(lambda: self.flip_friendly_in_lane())
            ])

        def flip_friendly_in_lane(self):
            for card in self.card.host.cards:
                card.minion.flip_up()

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
