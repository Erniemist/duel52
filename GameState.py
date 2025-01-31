class GameState:
    def __init__(self, winner, graveyard, players, board, active_player_index):
        self.winner = winner
        self.graveyard = graveyard
        self.players = players
        self.board = board
        self.active_player_index = active_player_index
        self.triggers = []

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
        return next((card for card in self.board.get_cards() if card.card_id == card_id), None)

    def get_cards(self):
        return self.board.get_cards() + self.graveyard.get_cards() + self.get_hand_cards()

    def get_hand_cards(self):
        return [card for player in self.players for card in player.hand.cards]

    def trigger(self, trigger):
        self.triggers.append(trigger)

    def resolve_triggers(self):
        while len(self.triggers) > 0:
            trigger = self.triggers.pop()
            for card in self.get_cards():
                if card.type:
                    card.type.handle_triggers(trigger)

    def new_turn(self):
        self.active_player().end_turn()
        self.active_player_index = (self.active_player_index + 1) % 2
        self.active_player().start_turn()
