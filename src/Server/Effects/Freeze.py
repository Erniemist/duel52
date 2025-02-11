from Server.Effects.Effect import Effect


class Freeze(Effect):
    def __init__(self, minion):
        self.minion = minion
        super().__init__()

    def _resolve(self):
        self.minion.frozen = True
