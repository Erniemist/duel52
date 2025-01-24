from Board.Lane.Side.Minion.Minion import Minion


class Side:
    def __init__(self, game, lane, player):
        self.game = game
        self.lane = lane
        self.player = player
        self.team = player.team
        self.cards = []

    def can_place(self, game, card):
        return self.team == game.active_player().team and self.player.actions > 0

    def on_place(self, game, card):
        game.cursor.card = None
        game.active_player().play_card(self, card)

    def add_card(self, card):
        card.minion = Minion(card, self, self.game)
        self.cards.append(card)

    def remove_card(self, card):
        card.minion = None
        self.cards = [c for c in self.cards if c is not card]
