class Trigger:
    def __init__(self, source_id, player):
        self.source_id = source_id
        self.player = player

    def source_is(self, card):
        return self.source_id == card.card_id
