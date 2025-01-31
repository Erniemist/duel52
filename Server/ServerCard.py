from Card.CardTypes.Three import Three
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Server.ServerSide import ServerSide
    from Server.ServerMinion import ServerMinion
    from Server.ServerGameState import ServerGameState
    from Deck.Deck import Deck
    from Graveyard.Graveyard import Graveyard
    from Hand.Hand import Hand


class ServerCard:
    types = {
        Three.value: Three,
    }

    def __init__(self, value: str, host, card_id: str, game):
        self.type: None | Three = None
        if value in self.types:
            self.type = self.types[value](self)
        self.value = value
        self.host: Deck | Hand | ServerSide | Graveyard = host
        self.card_id = card_id
        self.game: ServerGameState = game
        self.minion: None | ServerMinion = None
        self.minion_last_info: None | dict = None

    def move_to(self, new_host):
        old_host = self.host
        self.host = new_host
        self.host.add_card(self)
        old_host.remove_card(self)

    def to_json(self, player):
        data: dict = {'card_id': self.card_id}
        if player.knows(self):
            data['value'] = self.value
        if self.minion:
            data['minion'] = self.minion.to_json()
        return data
