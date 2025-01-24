from Hand.HandView import HandView


class Hand:
    def __init__(self, player):
        self.player = player
        self.team = player.team
        self.cards = []

    def view(self):
        return HandView(self, self.player.game.screen.get_width() / 2, self.player.game.screen.get_height() * 0.9)

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]
