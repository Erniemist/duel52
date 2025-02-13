from Server.Ability import Ability
from Server.CardTypes.CardType import CardType
from Server.Effects.Effect import Effect
from Server.Triggers.AttackTrigger import AttackTrigger


class Eight(CardType):
    """When this card is attacked, it deals 1 damage to the attacker"""
    value = '8'

    class Ability1(Ability):
        @staticmethod
        def should_trigger(card, trigger):
            return isinstance(trigger, AttackTrigger) and trigger.defender_id == card.card_id

        def __init__(self, card, game, trigger):
            self.player = trigger.player
            self.attacker = game.find_card_from_board(trigger.source_id).minion
            super().__init__(parts=[
                Effect(lambda: self.attacker.take_damage(1))
            ])

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability1])
