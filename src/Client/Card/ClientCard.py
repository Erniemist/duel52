from typing import TYPE_CHECKING

from Client.Board.Lane.Side.Minion.ClientMinion import ClientMinion

if TYPE_CHECKING:
    from Client.Board.Lane.Side.ClientSide import ClientSide
    from Client.ClientGameState import ClientGameState
    from Client.Deck.Deck import Deck
    from Client.Graveyard.Graveyard import Graveyard
    from Client.Hand.Hand import Hand


class ClientCard:
    def __init__(self, value: str, host, card_id: str, game, minion_data: None | dict = None):
        self.value = value
        self.host: Deck | Graveyard | Hand | ClientSide = host
        self.card_id = card_id
        self.game: ClientGameState = game
        if minion_data is not None:
            self.minion = ClientMinion.from_json(card=self, side=host, game=game, data=minion_data)
        else:
            self.minion = None

    def can_select(self, my_turn):
        return (
            my_turn
            and self.game.active_player().team == self.host.player.team
            and self.game.active_player().actions > 0
        )

    def on_select(self, cursor):
        cursor.pick_up(self)

    @staticmethod
    def from_json(host, game, data):
        minion_data = data['minion'] if 'minion' in data.keys() else None

        return ClientCard(
            value=data['value'],
            host=host,
            card_id=data['card_id'],
            game=game,
            minion_data=minion_data,
        )
