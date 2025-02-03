from Client.Card.ClientCard import ClientCard
from Server.ServerCard import ServerCard


class Graveyard:
    def __init__(self, game, cards_data):
        self.game = game
        self.cards = {
            card_data['card_id']: ClientCard.from_json(host=self, game=game, data=card_data)
            for card_data in cards_data
        }

    def add_card(self, card):
        self.cards[card.card_id] = card

    def remove_card(self, card):
        self.cards.pop(card.card_id)

    def get_cards(self):
        return [self.cards[key] for key in self.cards.keys()]

    def to_json(self, for_player):
        return {'cards': [card.to_json(for_player) for card in self.cards.values()]}

    @staticmethod
    def from_json(game, data):
        return Graveyard(game=game, cards_data=data['cards'])

    @staticmethod
    def from_json_server(game, data):
        graveyard = Graveyard(game=game, cards_data=data['cards'])
        graveyard.cards = {
            card_data['card_id']: ServerCard.from_json(host=graveyard, game=game, data=card_data)
            for card_data in data['cards']
        }
        return graveyard
