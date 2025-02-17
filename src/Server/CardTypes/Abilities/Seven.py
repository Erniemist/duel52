from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Effects.Effect import Effect


class Seven(OnFlip):
    description = 'When this card flips, heal ALL friendly minions.'

    def __init__(self, card, game, trigger):
        self.player = trigger.player
        super().__init__(parts=[
            Effect(lambda: self.heal_all_friendly())
        ])

    def heal_all_friendly(self):
        for minion in self.player.minions():
            minion.hp = minion.max_hp
