class FromHand:
    name = 'FromHand'

    def __init__(self, player):
        self.player = player
        self.card = None
        self.resolved = False

    def submit(self, card_id, game):
        self.card = game.find_card_from_hand(card_id)
        if self.card is None:
            raise Exception(f'Card {card_id} not found in hand')
        self.resolved = True

    def could_choose_minion(self, minion):
        return False

    def could_choose_card(self, card):
        return self.player.hand.contains(card)
