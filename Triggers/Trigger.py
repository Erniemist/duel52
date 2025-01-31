class Trigger:
    def __init__(self, card_id):
        self.card_id = card_id

    def source_is(self, card):
        return self.card_id == card.card_id
