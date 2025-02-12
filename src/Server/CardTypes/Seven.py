from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect
from Server.Triggers.FlipTrigger import FlipTrigger


class Seven(CardType):
    """When this card flips, heal ALL friendly minions."""
    value = '7'

    class Ability1(Ability):
        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

        def __init__(self, card, game, player):
            self.player = player
            super().__init__(parts=[
                Effect(lambda: self.heal_all_friendly())
            ])

        def heal_all_friendly(self):
            for minion in self.player.minions():
                minion.hp = minion.max_hp

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
