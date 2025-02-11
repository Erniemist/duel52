from Server.Effects.Effect import Effect


class FlipUp(Effect):
    def __init__(self, card):
        self.card = card
        super().__init__()

    def _resolve(self):
        self.card.minion.flip_up()
