from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Discard import Discard
from Server.Effects.Draw import Draw
from Server.Triggers.FlipTrigger import FlipTrigger


class Two(CardType):
    """When this card flips, draw a card, then discard a card."""

    class Ability1(Ability):
        def __init__(self, card, game, player):
            super().__init__(effects=[Draw(player), Discard(game, player)])

        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

    value = '2'

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
