from Server.Choices.Validator import Validator


class FromHand(Validator):
    name = 'FromHand'

    def __init__(self, player):
        self.player = player
        super().__init__()

    def could_choose(self, card):
        return self.player.hand.contains(card)
