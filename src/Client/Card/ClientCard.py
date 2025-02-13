from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Client.Board.Lane.Side.ClientSide import ClientSide
    from Client.ClientGameState import ClientGameState
    from Client.Deck.Deck import Deck
    from Client.Graveyard.ClientGraveyard import ClientGraveyard
    from Client.Hand.Hand import Hand


class ClientCard:
    def __init__(self, game, host, card_data):
        self.value = card_data.value
        self.host: Deck | ClientGraveyard | Hand | ClientSide = host
        self.card_id = card_data.card_id
        self.game: ClientGameState = game
        self.minion = None

    def can_select(self, my_turn):
        return (
            my_turn
            and self.game.active_player().team == self.host.player.team
            and self.game.active_player().actions > 0
        )

    def can_choose(self, choice):
        return choice.could_choose(self)

    def on_select(self, cursor):
        cursor.pick_up(self)

    def on_choose(self):
        return self.game.submit_choice(self.card_id)