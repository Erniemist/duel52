from Client.Card.ClientCard import ClientCard
from Server.ServerCard import ServerCard


class Deck:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.cards = []

    def draw_from_top(self, zone):
        if len(self.cards) == 0:
            return
        self.cards[0].move_to(zone)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]

    def add_card(self, card):
        self.cards.append(card)

    def to_json(self, for_player):
        return {'cards': [card.to_json(for_player) for card in self.cards]}

    @staticmethod
    def from_json(game, player, data):
        deck = Deck(game=game, player=player)
        deck.cards = [ClientCard.from_json(host=deck, game=game, data=card_data) for card_data in data['cards']]
        return deck

    @staticmethod
    def from_json_server(game, player, data):
        deck = Deck(game=game, player=player)
        deck.cards = [ServerCard.from_json(host=deck, game=game, data=card_data) for card_data in data['cards']]
        return deck
