from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.FlipUp import FlipUp
from Server.Triggers.FlipTrigger import FlipTrigger


class Five(CardType):
    """When this card flips, flip all friendly minions in the same lane."""
    value = '5'

    class Ability1(Ability):
        def __init__(self, card, game, player):
            super().__init__(effects=[
                FlipUp(other_card)
                for other_card in card.host.cards
                if other_card.minion.face_down
            ])

        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
