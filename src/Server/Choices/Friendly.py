from Server.Choices.Validator import Validator


class Friendly(Validator):
    name = 'Friendly'

    def __init__(self, card):
        super().__init__(card)

    def could_choose(self, card):
        return card.minion.team == self.card.minion.team
