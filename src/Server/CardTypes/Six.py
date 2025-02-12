from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect
from Server.Triggers.FlipTrigger import FlipTrigger


class Six(CardType):
    """When this card flips, freeze all enemy minions in the same lane."""
    value = '6'

    class Ability1(Ability):
        def __init__(self, card, game, player):
            self.card = card
            super().__init__(parts=[
                Effect(lambda: self.freeze_all_enemy_in_lane())
            ])

        def freeze_all_enemy_in_lane(self):
            for other_card in self.card.host.other_side().cards:
                other_card.minion.frozen = True

        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, FlipTrigger) and trigger.source_is(card)

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
