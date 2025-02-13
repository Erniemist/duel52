class Friendly:
    name = 'Friendly'

    def __init__(self, team):
        self.team = team

    def could_choose(self, card):
        return card.minion.team == self.team
