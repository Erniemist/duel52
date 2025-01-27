import json

from Card.Card import Card


class Graveyard:
    def __init__(self, game):
        self.game = game
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def to_json(self):
        return {
            'cards': [card.to_json() for card in self.cards]
        }

    @staticmethod
    def from_json(game, data):
        graveyard = Graveyard(game=game)
        graveyard.cards = [Card.from_json(host=graveyard, game=game, data=card_data) for card_data in data['cards']]
        return graveyard
