class Trigger:
    def __init__(self, card_id, player):
        self.card_id = card_id
        self.player = player

    def source_is(self, card):
        return self.card_id == card.card_id
