from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Freeze import Freeze
from Server.Triggers.FlipTrigger import FlipTrigger


class Six(CardType):
    """When this card flips, freeze all enemy minions in the same lane."""
    value = '6'

    class Ability1(Ability):
        def __init__(self, card, game, player):
            super().__init__(effects=[
                Freeze(other_card.minion)
                for other_card in card.host.other_side().cards
            ])

        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
