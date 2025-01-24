from Hand.HandView import HandView


class Hand:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.team = player.team
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]
