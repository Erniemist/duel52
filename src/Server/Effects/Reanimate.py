from Server.Effects.Effect import Effect


class Reanimate(Effect):
    def __init__(self, card, side):
        self.card = card
        self.side = side
        super().__init__()

    def _resolve(self):
        self.card.move_to(self.side)
