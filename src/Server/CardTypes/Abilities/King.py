from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Effects.Effect import Effect
from Server.Triggers.FlipTrigger import FlipTrigger


class King(OnFlip):
    value = 'K'
    description = 'When this card flips, retrigger the flip abilities of all friendly non-king minions in the same lane.'

    def __init__(self, card, game, trigger):
        self.game = game
        self.card = card
        self.player = trigger.player
        super().__init__(parts=[
            Effect(lambda: self.repeat_battlecries())
        ])

    def repeat_battlecries(self):
        for card in self.card.host.cards:
            if card.value != King.value:
                self.game.trigger(FlipTrigger(card.card_id, self.player))
