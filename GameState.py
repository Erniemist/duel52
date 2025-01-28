class GameState:
    def __init__(self):
        self.graveyard = None
        self.players = []
        self.board = None
        self.active_player_index = 0
        self.winner = None

    def active_player(self):
        return self.players[self.active_player_index]

    def find_card_from_hand(self, card_id):
        for player in self.players:
            for card in player.hand.cards:
                if card.card_id == card_id:
                    return card
        return None

    def find_card_from_board(self, card_id):
        for lane in self.board.lanes:
            for side in lane.sides:
                card = side.find_card(card_id)
                if card:
                    return card
        return None
