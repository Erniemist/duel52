from Server.CardTypes.Abilities.Stealth import Stealth
from Server.CardTypes.card_types import get_type
from Server.MinionLastInfo import MinionLastInfo
from Server.ServerMinion import ServerMinion
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Server.ServerSide import ServerSide
    from Server.ServerGameState import ServerGameState
    from Client.Deck.Deck import Deck
    from Client.Graveyard.ClientGraveyard import ClientGraveyard
    from Client.Hand.Hand import Hand


class ServerCard:
    def __init__(self, game, host, card_data):
        self.type = get_type(card_data.value)(self)
        self.value = card_data.value
        self.host: Deck | Hand | ServerSide | ClientGraveyard = host
        self.card_id = card_data.card_id
        self.game: ServerGameState = game
        self.minion: None | ServerMinion = None
        self.minion_last_info = None

    def move_to(self, new_host):
        old_host = self.host
        if self.minion is not None:
            self.minion_last_info = MinionLastInfo(self.minion)
        self.host = new_host
        old_host.remove_card(self)
        self.host.add_card(self)

    def has_keyword(self, keyword):
        return any(ability == keyword for ability in self.type.abilities)

    def can_see(self, other):
        team = self.minion.team if self.minion else self.minion_last_info.team
        return team == other.team or not other.has_active_keyword(Stealth)
