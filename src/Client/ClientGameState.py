from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Client.App import App
from Client.Board.ClientBoard import ClientBoard
from Client.Graveyard.Graveyard import Graveyard
from Client.Player.ClientPlayer import ClientPlayer
from Client.Card.ClientCard import ClientCard


class ClientGameState:
    def __init__(self, game_data, app):
        graveyard, players, board = game_data.build_for_client(self)
        self.winner = game_data.winner
        self.graveyard: Graveyard = graveyard
        self.players: list[ClientPlayer] = players
        self._active_player: ClientPlayer = self.players[game_data.active_player_index]
        self.board: ClientBoard = board
        self.app: App = app

    def active_player(self):
        return self._active_player

    def find_card_from_board(self, card_id) -> None | ClientCard:
        return next((card for card in self.board.get_cards() if card.card_id == card_id))

    def find_card_from_hand(self, card_id) -> None | ClientCard:
        for player in self.players:
            for card in player.hand.cards:
                if card.card_id == card_id:
                    return card
        return None

    def play_event(self, card, side):
        self.app.event('play', {'card': card.card_id, 'side': side.side_id})

    def flip_event(self, minion):
        self.app.event('flip', {'card': minion.card.card_id})

    def attack_event(self, minion_1, minion_2):
        self.app.event('attack', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})

    def pair_event(self, minion_1, minion_2):
        self.app.event('pair', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})
