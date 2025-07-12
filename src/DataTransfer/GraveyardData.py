from Client.Card.ClientCard import ClientCard
from Client.Graveyard.ClientGraveyard import ClientGraveyard
from DataTransfer.CardData import CardData
from Server.ServerCard import ServerCard
from Server.ServerGraveyard import ServerGraveyard


class GraveyardData:
    def __init__(self, cards):
        self.cards = cards
        self.is_server = None

    @staticmethod
    def from_json(data):
        return GraveyardData(cards=[CardData.from_json(card) for card in data['cards']])

    def make(self, game, is_server):
        self.is_server = is_server
        return ServerGraveyard(game, self) if is_server else ClientGraveyard(game, self)

    @staticmethod
    def from_server(graveyard: ServerGraveyard, for_player):
        return GraveyardData(cards=[CardData.from_server(card, for_player) for card in graveyard.cards.values()])

    def build(self, game, graveyard):
        assert self.is_server is not None
        return {
            card_data.card_id: card_data.make(game=game, host=graveyard, is_server=self.is_server)
            for card_data in self.cards
        }

    def to_json(self):
        return {'cards': [card.to_json() for card in self.cards]}
