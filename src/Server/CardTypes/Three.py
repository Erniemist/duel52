from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.FlipUp import FlipUp
from Server.Effects.Reanimate import Reanimate
from Server.Triggers.DeathTrigger import DeathTrigger


class Three(CardType):
    """When this card dies face down, return it to its lane face up."""
    value = '3'

    class Ability1(Ability):
        def __init__(self, card, game, player):
            super().__init__(effects=[Reanimate(card, side=card.minion_last_info.side), FlipUp(card)])

        @staticmethod
        def should_trigger(card, trigger):
            return (
                isinstance(trigger, DeathTrigger)
                and trigger.source_is(card)
                and card.minion_last_info.face_down
            )

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
