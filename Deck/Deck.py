import json
import random

from Card.Card import Card


class Deck:
    def __init__(self, game, values=None):
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

    def to_json(self):
        return {
            'cards': [card.to_json() for card in self.cards]
        }

    @staticmethod
    def from_json(game, data):
        deck = Deck(game=game)
        deck.cards = [Card.from_json(host=deck, game=game, data=card_data) for card_data in data['cards']]
        return deck
