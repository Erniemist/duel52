from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Heal import Heal
from Server.Triggers.FlipTrigger import FlipTrigger


class Seven(CardType):
    """When this card flips, heal ALL friendly minions."""
    value = '7'

    class Ability1(Ability):
        def __init__(self, card, game, player):
            super().__init__(effects=[
                Heal(minion)
                for minion in card.minion.player.minions()
            ])

        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
