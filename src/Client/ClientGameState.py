from Client.Board.ClientBoard import ClientBoard
from Client.Card.ClientCard import ClientCard
from Client.Graveyard.ClientGraveyard import ClientGraveyard
from Client.Player.ClientPlayer import ClientPlayer


class ClientGameState:
    def __init__(self, game_data):
        graveyard, players, board = game_data.build(self)
        self.winner = game_data.winner
        self.graveyard: ClientGraveyard = graveyard
        self.players: list[ClientPlayer] = players
        self._active_player: ClientPlayer = self.players[game_data.active_player_index]
        self.board: ClientBoard = board
        self.actions = []

    def active_player(self):
        return self._active_player

    def find_card_from_board(self, card_id) -> None | ClientCard:
        return next((card for card in self.board.get_cards() if card.card_id == card_id), None)

    def find_card_from_hand(self, card_id) -> None | ClientCard:
        for player in self.players:
            for card in player.hand.cards:
                if card.card_id == card_id:
                    return card
        return None

    def play_action(self, card, side):
        self.actions.append(PlayAction(card.card_id, side.side_id))

    def flip_action(self, minion):
        self.actions.append(FlipAction(minion.card.card_id))

    def attack_action(self, minion_1, minion_2):
        self.actions.append(AttackAction(minion_1.card.card_id, minion_2.card.card_id))

    def pair_action(self, minion_1, minion_2):
        self.actions.append(PairAction(minion_1.card.card_id, minion_2.card.card_id))
