class FromHand:
    name = 'FromHand'

    def __init__(self, player):
        self.player = player

    def could_choose(self, card):
        return self.player.hand.contains(card)
