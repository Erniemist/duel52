from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect
from Server.Triggers.FlipTrigger import FlipTrigger


class Ace(CardType):
    """When this card flips, gain an action. This card may attack twice if it flipped this turn."""
    value = 'A'

    class Ability1(Ability):
        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

        def __init__(self, card, game, player):
            self.card = card
            self.player = player
            super().__init__(parts=[
                Effect(lambda: self.gain_action()),
                Effect(lambda: self.gain_attack()),
            ])

        def gain_action(self):
            self.player.actions += 1

        def gain_attack(self):
            self.card.minion.max_attacks = 2

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
