from Server.Ability import Ability
from Server.Effects.Effect import Effect
from Server.Triggers.DeathTrigger import DeathTrigger


class Three(Ability):
    description = 'When this card dies face down, return it to its lane face up.'

    @staticmethod
    def should_trigger(card, trigger):
        return (
            isinstance(trigger, DeathTrigger)
            and trigger.source_is(card)
            and card.minion_last_info.face_down
        )

    def __init__(self, card, game, trigger):
        self.card = card
        self.reanimated_minion = None
        super().__init__(parts=[
            Effect(lambda: self.reanimate()),
            Effect(lambda: self.reanimated_minion.flip_up()),
        ])

    def reanimate(self):
        self.card.move_to(self.card.minion_last_info.side)
        self.reanimated_minion = self.card.minion
