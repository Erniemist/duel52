from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Choices.CardChoice import CardChoice
from Server.Choices.FromHand import FromHand
from Server.Effects.Effect import Effect
from Server.Effects.effects import discard, draw
from Server.Triggers.FlipTrigger import FlipTrigger


class Two(CardType):
    """When this card flips, draw a card, then discard a card."""
    value = '2'

    class Ability1(Ability):
        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

        def __init__(self, card, game, player):
            self.discard_choice = CardChoice([FromHand(player)], game, player)
            super().__init__(
                [
                    Effect(lambda: draw(player)),
                    self.discard_choice,
                    Effect(lambda: discard(game, self.discard_choice.card)),
                ],
            )

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
