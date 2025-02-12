from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect
from Server.Triggers.FlipTrigger import FlipTrigger


class King(CardType):
    """When this card flips, retrigger the flip abilities of all friendly non-king minions in the same lane."""
    value = 'K'

    class Ability1(Ability):
        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

        def __init__(self, card, game, player):
            self.game = game
            self.card = card
            self.player = player
            super().__init__(parts=[
                Effect(lambda: self.repeat_battlecries())
            ])

        def repeat_battlecries(self):
            for card in self.card.host.cards:
                if card.type.value != King.value:
                    self.game.trigger(FlipTrigger(card.card_id, self.player))

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
