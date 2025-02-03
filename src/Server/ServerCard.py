from Client.Card.CardTypes.Three import Three
from Server.ServerMinion import ServerMinion
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Server.ServerSide import ServerSide
    from Server.ServerGameState import ServerGameState
    from Client.Deck.Deck import Deck
    from Client.Graveyard.ClientGraveyard import ClientGraveyard
    from Client.Hand.Hand import Hand


class ServerCard:
    types = {
        Three.value: Three,
    }

    def __init__(self, value: str, host, card_id: str, game):
        self.type: None | Three = None
        if value in self.types:
            self.type = self.types[value](self)
        self.value = value
        self.host: Deck | Hand | ServerSide | ClientGraveyard = host
        self.card_id = card_id
        self.game: ServerGameState = game
        self.minion: None | ServerMinion = None
        self.minion_last_info: None | dict = None

    def move_to(self, new_host):
        old_host = self.host
        self.host = new_host
        self.host.add_card(self)
        old_host.remove_card(self)

    def to_json(self, for_player):
        data: dict = {
            'card_id': self.card_id,
            'value': self.value if for_player.knows(self) else '',
        }
        if self.minion:
            data['minion'] = self.minion.to_json()
        return data

    @staticmethod
    def from_json(game, host, data):
        card = ServerCard(data['value'], host, data['card_id'], game)
        if 'minion' in data.keys():
            card.minion = ServerMinion(card, host, game)
            card.minion.hp = data['minion']['hp']
            card.minion.face_down = data['minion']['face_down']
            card.minion.attacks_made = data['minion']['attacks_made']
            if 'pair' in data['minion'].keys():
                for other in host.cards:
                    if other.card_id == data['minion']['pair']:
                        card.minion.pair_with(other.minion)
                        break
        return card
