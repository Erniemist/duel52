from typing import TYPE_CHECKING

from Client.Actions.PlayAction import PlayAction
from Server.CardTypes.card_types import get_type

if TYPE_CHECKING:
    from Client.Board.Lane.Side.ClientSide import ClientSide
    from Client.ClientGameState import ClientGameState
    from Client.Deck.Deck import Deck
    from Client.Graveyard.ClientGraveyard import ClientGraveyard
    from Client.Hand.Hand import Hand


class ClientCard:
    def __init__(self, game, host, card_data):
        self.value = card_data.value
        self.type = get_type(card_data.value)(self)
        self.host: Deck | ClientGraveyard | Hand | ClientSide = host
        self.card_id = card_data.card_id
        self.game: ClientGameState = game
        self.minion = None

    def can_select(self):
        return any(
            proposal['action'] == PlayAction.name
            and proposal['data']['card'] == self.card_id
            for proposal in self.game.proposals
        )

    def can_hover(self, player):
        return self.card_id in player.known_cards

    def on_hover(self):
        pass

    def can_choose(self, choice):
        return self in choice.cards

    def on_select(self, cursor):
        cursor.pick_up(self)

    def on_choose(self):
        return self.game.submit_choice(self.card_id)

    def has_keyword(self, keyword):
        return any(ability == keyword for ability in self.type.abilities)
