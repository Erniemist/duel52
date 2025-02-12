class FromBoard:
    name = 'FromBoard'

    def __init__(self, game):
        self.game = game

    def could_choose(self, card):
        return self.game.find_card_from_board(card.card_id) is not None
