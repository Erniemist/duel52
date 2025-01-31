class Board:
    def __init__(self, game, lanes):
        self.game = game
        self.lanes = lanes

    def get_cards(self):
        return [card for lane in self.lanes for card in lane.get_cards()]
