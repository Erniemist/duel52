from Client.Card.ClientCard import ClientCard
from Server.ServerCard import ServerCard


class CardData:
    def __init__(self, card_id, value):
        self.card_id = card_id
        self.value = value
        self.game = None
        self.host = None
        self.is_server = None

    @staticmethod
    def from_json(data):
        return CardData(
            card_id=data['card_id'],
            value=data['value'],
        )

    def make(self, game, host, is_server):
        self.game = game
        self.host = host
        self.is_server = is_server
        return ServerCard(game, host, self) if is_server else ClientCard(game, host, self)

    @staticmethod
    def from_server(card: ServerCard, for_player):
        return CardData(
            card_id=card.card_id,
            value=card.value if for_player.knows(card) else '',
        )

    def to_json(self):
        return {
            'card_id': self.card_id,
            'value': self.value,
        }
