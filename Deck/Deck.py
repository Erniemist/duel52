import random

from Card.Card import Card
from Deck.DeckView import DeckView


class Deck:
    def __init__(self, player):
        self.player = player
        self.deck = [
            Card(value, self)
            for value in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        ]
        random.shuffle(self.deck)

    def view(self):
        return DeckView(self, 150, self.player.game.screen.get_height() * 0.85)

    def on_select(self, game):
        self.deck[0].move_to(self.player.hand)

    def remove_card(self, card):
        self.deck = [c for c in self.deck if c is not card]
