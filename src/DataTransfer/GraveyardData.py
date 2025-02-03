from Client.Card.ClientCard import ClientCard
from Client.Graveyard.ClientGraveyard import ClientGraveyard
from Server.ServerCard import ServerCard
from Server.ServerGraveyard import ServerGraveyard


class GraveyardData:
    def __init__(self, cards):
        self.cards = cards

    @staticmethod
    def from_json(data):
        return GraveyardData(cards=data['cards'])

    def make_server(self, game):
        return ServerGraveyard(game, self)

    def build_for_server(self, game, graveyard):
        return {
            card_data['card_id']: ServerCard.from_json(host=graveyard, game=game, data=card_data)
            for card_data in self.cards
        }

    @staticmethod
    def from_server(graveyard: ServerGraveyard, for_player):
        return GraveyardData(cards=[card.to_json(for_player) for card in graveyard.cards.values()])

    def make_client(self, game):
        return ClientGraveyard(game, self)

    def build_for_client(self, game, graveyard):
        return {
            card_data['card_id']: ClientCard.from_json(host=graveyard, game=game, data=card_data)
            for card_data in self.cards
        }

    def to_json(self):
        return {'cards': self.cards}
