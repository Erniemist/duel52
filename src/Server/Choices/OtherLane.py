from Server.Choices.Validator import Validator


class OtherLane(Validator):
    name = 'OtherLane'

    def could_choose(self, card):
        return card.minion and card.minion.side.lane is not self.card.minion.side.lane
