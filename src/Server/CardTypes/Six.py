from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect


class Six(CardType):
    """When this card flips, freeze all enemy minions in the same lane."""
    value = '6'

    class Ability(OnFlip):
        def __init__(self, card, game, trigger):
            self.card = card
            super().__init__(parts=[
                Effect(lambda: self.freeze_all_enemy_in_lane())
            ])

        def freeze_all_enemy_in_lane(self):
            for other_card in self.card.host.other_side().cards:
                other_card.minion.frozen = True

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability])
