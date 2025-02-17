from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Effects.Effect import Effect


class Ace(OnFlip):
    description = 'When this card flips, gain an action. This card may attack twice if it flipped this turn.'

    def __init__(self, card, game, trigger):
        self.card = card
        self.player = trigger.player
        super().__init__(parts=[
            Effect(self.gain_action),
            Effect(self.gain_attack),
        ])

    def gain_action(self):
        self.player.actions += 1

    def gain_attack(self):
        self.card.minion.max_attacks = 2
