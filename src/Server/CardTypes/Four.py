from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Choices.FromBoard import FromBoard
from Server.Effects.Effect import Effect
from Server.Triggers.FlipTrigger import FlipTrigger


class Four(CardType):
    """When this card flips, look at a facedown card."""
    value = '4'

    class Ability1(Ability):
        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

        def __init__(self, card, game, player):
            self.player = player
            self.peek_choice = FromBoard(player)
            super().__init__(
                [
                    self.peek_choice,
                    Effect(lambda: self.player.learn(self.peek_choice.minion.card)),
                ],
            )

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
