class Deck:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.cards = []

    def draw_from_top(self, zone):
        if len(self.cards) == 0:
            return
        self.cards[0].move_to(zone)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]

    def add_card(self, card):
        self.cards.append(card)
