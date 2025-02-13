class OtherLane:
    name = 'OtherLane'

    def __init__(self, card):
        self.card = card

    def could_choose(self, card):
        return card.minion and card.minion.side.lane is not self.card.minion.side.lane
