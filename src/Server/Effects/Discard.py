from Server.Choices.FromHand import FromHand
from Server.Effects.Effect import Effect


class Discard(Effect):
    def __init__(self, game, player):
        self.game = game
        self.card_to_discard = FromHand(player)
        super().__init__([self.card_to_discard])

    def _resolve(self):
        self.card_to_discard.choice.move_to(self.game.graveyard)
