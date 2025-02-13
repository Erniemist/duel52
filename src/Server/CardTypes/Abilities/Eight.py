from Server.Ability import Ability
from Server.Effects.Effect import Effect
from Server.Triggers.AttackTrigger import AttackTrigger


class Eight(Ability):
    description = 'When this card is attacked, it deals 1 damage to the attacker'

    @staticmethod
    def should_trigger(card, trigger):
        return isinstance(trigger, AttackTrigger) and trigger.defender_id == card.card_id

    def __init__(self, card, game, trigger):
        self.player = trigger.player
        self.attacker = game.find_card_from_board(trigger.source_id).minion
        super().__init__(parts=[
            Effect(self.reflect_damage)
        ])

    def reflect_damage(self):
        if self.attacker.pair:
            self.attacker.take_damage(1)
            self.attacker.pair.take_damage(1)
        else:
            self.attacker.take_damage(1)
