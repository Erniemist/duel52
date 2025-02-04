from Client.Card.ClientCard import ClientCard
from Client.Graveyard.ClientGraveyard import ClientGraveyard
from Server.ServerCard import ServerCard
from Server.ServerGraveyard import ServerGraveyard


class GraveyardData:
    def __init__(self, cards):
        self.cards = cards
        self.is_server = None

    @staticmethod
    def from_json(data):
        return GraveyardData(cards=data['cards'])

    def make(self, game, is_server):
        self.is_server = is_server
        return ServerGraveyard(game, self) if is_server else ClientGraveyard(game, self)

    @staticmethod
    def from_server(graveyard: ServerGraveyard, for_player):
        return GraveyardData(cards=[card.to_json(for_player) for card in graveyard.cards.values()])

    def build(self, game, graveyard):
        assert self.is_server is not None
        card = ServerCard if self.is_server else ClientCard
        return {
            card_data['card_id']: card.from_json(host=graveyard, game=game, data=card_data)
            for card_data in self.cards
        }

    def to_json(self):
        return {'cards': self.cards}
