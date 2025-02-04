from Client.Board.ClientBoard import ClientBoard
from Client.Board.Lane.ClientLane import ClientLane
from Client.Board.Lane.Side.ClientSide import ClientSide
from Client.Board.Lane.Side.Minion.ClientMinion import ClientMinion
from Client.Card.ClientCard import ClientCard
from Server.ServerBoard import ServerBoard
from Server.ServerCard import ServerCard
from Server.ServerLane import ServerLane
from Server.ServerMinion import ServerMinion
from Server.ServerSide import ServerSide


class CardData:
    def __init__(self, card_id, value, minion=None):
        self.card_id = card_id
        self.value = value
        self.minion: dict = minion
        self.game = None
        self.host = None
        self.is_server = None

    @staticmethod
    def from_json(data):
        return CardData(
            card_id=data['card_id'],
            value=data['value'],
            minion=data['minion'] if 'minion' in data.keys() else None,
        )

    def make(self, game, host, is_server):
        self.game = game
        self.host = host
        self.is_server = is_server
        return ServerCard(game, host, self) if is_server else ClientCard(game, host, self)

    @staticmethod
    def from_server(card: ServerCard, for_player):
        if card.minion is None:
            minion = None
        else:
            minion = {
                'hp': card.minion.hp,
                'face_down': card.minion.face_down,
                'attacks_made': card.minion.attacks_made,
            }
            if card.minion.pair:
                minion['pair'] = card.minion.pair.card.card_id
        return CardData(
            card_id=card.card_id,
            value=card.value if for_player.knows(card) else '',
            minion=minion,
        )

    def build(self, card):
        assert self.is_server is not None
        if self.minion is None:
            return None

        minion_type = ServerMinion if self.is_server else ClientMinion
        minion = minion_type(card, self.host, self.game, self.minion)
        if 'pair' in self.minion.keys():
            for other in self.host.cards:
                if other.card_id == self.minion['pair']:
                    minion.pair_with(other.minion)
                    break
        return minion

    def to_json(self):
        data = {
            'card_id': self.card_id,
            'value': self.value,
        }
        if self.minion:
            data['minion'] = self.minion
        return data
