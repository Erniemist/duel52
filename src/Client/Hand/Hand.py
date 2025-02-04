class Hand:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        self.player.learn(card)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]
