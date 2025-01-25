import random

from Card.Card import Card


class Deck:
    def __init__(self, game, values=None):
        self.player = None
        self.game = game
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4 if values is None else values
        self.cards = [
            Card(value, self)
            for value in values
        ]
        random.shuffle(self.cards)

    def draw_from_top(self, zone):
        self.cards[0].move_to(zone)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]

    def add_card(self, card):
        self.cards.append(card)
