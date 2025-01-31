class Lane:
    def __init__(self, game, players, lane_id, sides):
        self.game = game
        self.players = players
        self.lane_id = lane_id
        self.sides = sides

    def get_cards(self):
        return [card for side in self.sides for card in side.cards]
