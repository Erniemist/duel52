class FromHand:
    name = 'FromHand'

    def __init__(self, player):
        self.player = player
        self.choice = None

    def submit(self, card_id, game):
        self.choice = game.find_card_from_hand(card_id)
        if self.choice is None:
            raise Exception(f'Card {card_id} not found in hand')

    def could_choose_minion(self, minion):
        return False

    def could_choose_card(self, card):
        return self.player.hand.contains(card)
