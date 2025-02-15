class Deck:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.cards = []

    def draw_from_top(self, zone):
        if not self.cards:
            return
        self.cards[0].move_to(zone)

    def remove_card(self, card):
        self.cards.remove(card)

    def add_card(self, card):
        self.cards.append(card)
