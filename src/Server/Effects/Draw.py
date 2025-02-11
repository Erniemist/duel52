from Server.Effects.Effect import Effect


class Draw(Effect):
    def __init__(self, player):
        self.player = player
        super().__init__()

    def _resolve(self):
        self.player.deck.draw_from_top(self.player.hand)
