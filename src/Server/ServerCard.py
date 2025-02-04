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

    def __init__(self, game, host, card_data):
        self.type: None | Three = None
        value = card_data.value
        if value in self.types:
            self.type = self.types[value](self)
        self.value = value
        self.host: Deck | Hand | ServerSide | ClientGraveyard = host
        self.card_id = card_data.card_id
        self.game: ServerGameState = game
        self.minion: None | ServerMinion = None
        self.minion_last_info: None | dict = None

    def move_to(self, new_host):
        old_host = self.host
        self.host = new_host
        self.host.add_card(self)
        old_host.remove_card(self)
