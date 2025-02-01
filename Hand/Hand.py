from Card.ClientCard import ClientCard
from Server.ServerCard import ServerCard


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

    def to_json(self, for_player):
        data = {'cards': [card.to_json(for_player) for card in self.cards]}
        return data

    @staticmethod
    def from_json(game, player, data):
        hand = Hand(game=game, player=player)
        hand.cards = [ClientCard.from_json(host=hand, game=game, data=card_data) for card_data in data['cards']]
        return hand

    @staticmethod
    def from_json_server(game, player, data):
        hand = Hand(game=game, player=player)
        hand.cards = [ServerCard.from_json(host=hand, game=game, data=card_data) for card_data in data['cards']]
        return hand
