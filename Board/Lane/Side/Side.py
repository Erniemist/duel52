import json

from Board.Lane.Side.Minion.Minion import Minion
from Card.Card import Card


class Side:
    def __init__(self, game, lane, player):
        self.game = game
        self.lane = lane
        self.player = player
        self.team = player.team
        self.cards = []

    def can_place(self, game, card):
        return self.team == game.active_player().team and self.player.actions > 0

    def on_place(self, game, card):
        game.cursor.card = None
        game.active_player().play_card(self, card)

    def add_card(self, card):
        card.minion = Minion(card, self, self.game)
        self.cards.append(card)

    def remove_card(self, card):
        card.minion = None
        self.cards = [c for c in self.cards if c is not card]

    def index_card(self, card):
        return self.cards.index(card)

    def to_json(self):
        return {
            'cards': [card.to_json() for card in self.cards]
        }

    @staticmethod
    def from_json(lane, player, game, data):
        side = Side(game=game, lane=lane, player=player)
        side.cards = [Card.from_json(host=side, game=game, data=card_data) for card_data in data['cards']]
        for card, card_data in zip(side.cards, data['cards']):
            if 'pair' in card_data['minion'].keys() and not card.minion.pair:
                paired = side.cards[card_data['minion']['pair']].minion
                paired.pair = card.minion
                card.minion.pair = paired

        return side
