from Board.Lane.Side.Minion.Minion import Minion


class Side:
    def __init__(self, game, lane, team):
        self.lane = lane
        self.game = game
        self.team = team
        self.cards = []

    def can_place(self, game, card):
        return self.team == game.active_player.team

    def on_place(self, game, card):
        card.move_to(self)

    def add_card(self, card):
        card.minion = Minion(card, self, self.game)
        self.cards.append(card)

    def remove_card(self, card):
        card.minion = None
        self.cards = [c for c in self.cards if c is not card]
