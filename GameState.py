class GameState:
    def __init__(self, active_player_index):
        self.active_player_index = active_player_index

    def active_player(self):
        return self.players[self.active_player_index]

    def player_by_team(self, team):
        return next(player for player in self.players if player.team == team)

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
