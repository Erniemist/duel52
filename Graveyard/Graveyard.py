class Graveyard:
    def __init__(self, game):
        self.game = game
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
