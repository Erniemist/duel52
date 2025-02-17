from Server.Choices.Validator import Validator


class FromBoard(Validator):
    name = 'FromBoard'

    def __init__(self, game):
        self.game = game
        super().__init__()

    def could_choose(self, card):
        return self.game.find_card_from_board(card.card_id) is not None
