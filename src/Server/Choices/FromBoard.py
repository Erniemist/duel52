class FromBoard:
    name = 'FromBoard'

    def __init__(self, game):
        self.game = game
        self.minion = None
        self.resolved = False

    def submit(self, card_id, game):
        self.minion = game.find_card_from_board(card_id).minion
        if self.minion is None:
            raise Exception(f'Card {card_id} not found in board')
        self.resolved = True

    def could_choose_minion(self, minion):
        return self.game.find_card_from_board(minion.card_id) is not None

    def could_choose_card(self, card):
        return self.player.hand.contains(card)
