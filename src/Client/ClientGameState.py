from Client.Actions.AttackAction import AttackAction
from Client.Actions.ChooseAction import ChooseAction
from Client.Actions.FlipAction import FlipAction
from Client.Actions.PairAction import PairAction
from Client.Actions.PlayAction import PlayAction
from Client.Board.ClientBoard import ClientBoard
from Client.Card.ClientCard import ClientCard
from Client.Graveyard.ClientGraveyard import ClientGraveyard
from Client.Player.ClientPlayer import ClientPlayer
from Server.CardTypes.Abilities.Ten import Ten


class ClientGameState:
    def __init__(self, game_data):
        graveyard, players, board = game_data.build(self)
        self.winner = game_data.winner
        self.graveyard: ClientGraveyard = graveyard
        self.players: list[ClientPlayer] = players
        self._active_player: ClientPlayer = self.players[game_data.active_player_index]
        self.board: ClientBoard = board
        self.actions = []
        self.pending_attack = None

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
        self.actions.append(PlayAction(card, side))

    def flip_action(self, minion):
        self.actions.append(FlipAction(minion))

    def attack(self, attacker, target):
        if not attacker.card.has_keyword(Ten):
            self.actions.append(AttackAction(attacker, [target]))
            return
        if not self.pending_attack:
            self.pending_attack = AttackAction(attacker, [target])
            return
        if target.card.card_id != self.pending_attack.targets[0].card.card_id:
            self.pending_attack.targets.append(target)
        self.actions.append(self.pending_attack)
        self.pending_attack = None

    def pair_action(self, minion_1, minion_2):
        self.actions.append(PairAction(minion_1, minion_2))

    def submit_choice(self, card_id):
        self.actions.append(ChooseAction(card_id))
