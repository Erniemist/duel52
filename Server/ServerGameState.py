import random
import uuid

from Server.ServerBoard import ServerBoard
from Server.ServerCard import ServerCard
from Deck.Deck import Deck
from Graveyard.Graveyard import Graveyard
from Server.ServerPlayer import ServerPlayer


class ServerGameState:
    def __init__(self):
        self.winner: None | ServerPlayer = None
        self.graveyard: Graveyard = Graveyard(self, [])
        self.players: list[ServerPlayer] = self.make_players(self.make_deck())
        self.board: ServerBoard = ServerBoard(self, self.players)
        self.active_player_index = random.randint(0, 1)
        self.triggers = []
        self.active_player().start_turn(actions=2)

    def active_player(self) -> ServerPlayer:
        return self.players[self.active_player_index]

    def player_by_team(self, team):
        return next(player for player in self.players if player.team == team)

    def make_players(self, main_deck: Deck) -> list[ServerPlayer]:
        players = []
        for team in ['A', 'B']:
            player = ServerPlayer(team, self)
            for i in range(20):
                main_deck.draw_from_top(player.deck)
            for i in range(5):
                player.deck.draw_from_top(player.hand)
            players.append(player)
        return players

    def make_deck(self) -> Deck:
        main_deck = Deck(self, None)
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        cards = [
            ServerCard(value=value, host=main_deck, card_id=str(uuid.uuid4().int), game=self)
            for card_id, value in enumerate(values)
        ]
        random.shuffle(cards)
        main_deck.cards = cards
        return main_deck

    def check_victory(self):
        self.winner = self.determine_winner()

    def determine_winner(self) -> None | ServerPlayer:
        if not self.all_cards_played():
            return None
        lanes_won = {player.team: 0 for player in self.players}
        for lane in self.board.lanes:
            winner = lane.player_winning_lane()
            if winner is not None:
                lanes_won[winner.team] += 1
        for player in self.players:
            if lanes_won[player.team] > 1:
                return player
        return None

    def all_cards_played(self):
        return all(len(player.deck.cards) + len(player.hand.cards) == 0 for player in self.players)

    def find_side(self, side_id):
        for lane in self.board.lanes:
            for side in lane.sides:
                if side.side_id == side_id:
                    return side
        return None

    def find_card_from_board(self, card_id) -> ServerCard:
        return next((card for card in self.board.get_cards() if card.card_id == card_id))

    def find_card_from_hand(self, card_id) -> None | ServerCard:
        return next((card for card in self.get_hand_cards() if card.card_id == card_id), None)

    def get_hand_cards(self):
        return (card for player in self.players for card in player.hand.cards)

    def get_cards(self):
        yield from self.board.get_cards()
        yield from self.graveyard.get_cards()
        yield from self.get_hand_cards()

    def trigger(self, trigger):
        self.triggers.append(trigger)

    def resolve_triggers(self):
        while len(self.triggers) > 0:
            trigger = self.triggers.pop()
            for card in self.get_cards():
                if card.type:
                    card.type.handle_triggers(trigger)

    def new_turn(self):
        self.active_player().end_turn()
        self.active_player_index = (self.active_player_index + 1) % 2
        self.active_player().start_turn()

    @staticmethod
    def from_json(data):
        game = ServerGameState()
        game.winner = data['winner']
        game.active_player_index = data['active_player_index']
        game.players = [ServerPlayer.from_json(game, player_data) for player_data in data['players']]
        game.graveyard = Graveyard.from_json(game, data['graveyard'])
        game.board = ServerBoard.from_json(game, game.players, data['board'])
        return game

    def to_json(self, team):
        for_player = self.player_by_team(team)
        return {
            'active_player_index': self.active_player_index,
            'graveyard': self.graveyard.to_json(for_player=for_player),
            'players': [player.to_json(for_player=for_player) for player in self.players],
            'board': self.board.to_json(for_player=for_player),
            'winner': self.winner.team if self.winner else None,
        }

