from Client.Board.Lane.Side.Minion.ClientMinion import ClientMinion
from DataTransfer.CardData import CardData
from Server.ServerMinion import ServerMinion


class MinionCardData:
    def __init__(self, card, hp, face_down, attacks_made, frozen, pair=None):
        self.card = card
        self.hp = hp
        self.face_down = face_down
        self.attacks_made = attacks_made
        self.pair = pair
        self.frozen = frozen
        self.game = None
        self.side = None
        self.is_server = None

    @staticmethod
    def from_json(data):
        return MinionCardData(
            card=CardData.from_json(data),
            hp=data['minion']['hp'],
            face_down=data['minion']['face_down'],
            attacks_made=data['minion']['attacks_made'],
            frozen=data['minion']['frozen'],
            pair=data['minion']['pair'] if 'pair' in data['minion'].keys() else None,
        )

    def make(self, game, side, is_server):
        self.game = game
        self.side = side
        self.is_server = is_server
        card = self.card.make(game, side, is_server)
        card.minion = ServerMinion(card, side, game, self) if is_server else ClientMinion(card, side, game, self)
        if self.pair:
            other = next((card for card in side.cards if card.card_id == self.pair), None)
            if other is not None:
                card.minion.pair_with(other.minion)
        return card

    @staticmethod
    def from_server(minion: ServerMinion, for_player):
        return MinionCardData(
            card=CardData.from_server(minion.card, for_player),
            hp=minion.hp,
            face_down=minion.face_down,
            attacks_made=minion.attacks_made,
            frozen=minion.frozen,
            pair=minion.pair.card.card_id if minion.pair else None,
        )

    def to_json(self):
        data = {
            **self.card.to_json(),
            'minion': {
                'hp': self.hp,
                'face_down': self.face_down,
                'attacks_made': self.attacks_made,
                'frozen': self.frozen,
            }
        }
        if self.pair:
            data['minion']['pair'] = self.pair
        return data
