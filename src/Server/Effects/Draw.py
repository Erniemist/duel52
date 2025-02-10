from Server.Effects.Effect import Effect


class Draw(Effect):
    def _resolve(self):
        self.player.deck.draw_from_top(self.player.hand)
