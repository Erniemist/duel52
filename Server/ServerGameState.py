import random

from Board.Board import Board
from Server.ServerCard import ServerCard
from Deck.Deck import Deck
from Graveyard.Graveyard import Graveyard
from Server.ServerPlayer import ServerPlayer


class ServerGameState:
    def __init__(self):
        self.winner = None
        self.graveyard = Graveyard(self)
        self.players = self.make_players(self.make_deck())
        self.board = Board(self)
        self.active_player_index = random.randint(0, 1)
        self.active_player().start_turn(actions=2)

    def active_player(self):
        return self.players[self.active_player_index]

    def player_by_team(self, team):
        return next(player for player in self.players if player.team == team)

    def find_card_from_hand(self, card_id):
        for player in self.players:
            for card in player.hand.cards:
                if card.card_id == card_id:
                    return card
        return None

    def find_card_from_board(self, card_id):
        for lane in self.board.lanes:
            for side in lane.sides:
                card = side.find_card(card_id)
                if card:
                    return card
        return None

    def make_players(self, main_deck):
        players = []
        for team in ['A', 'B']:
            player = ServerPlayer(team, self)
            for i in range(20):
                main_deck.draw_from_top(player.deck)
            for i in range(5):
                player.deck.draw_from_top(player.hand)
            players.append(player)
        return players

    def make_deck(self):
        main_deck = Deck(self, None)
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        cards = [
            ServerCard(value=value, host=main_deck, card_id=card_id, game=self)
            for card_id, value in enumerate(values)
        ]
        random.shuffle(cards)
        main_deck.cards = cards
        return main_deck

    def check_victory(self):
        self.winner = self.determine_winner()

    def determine_winner(self):
        if not self.all_cards_played():
            return None
        lanes_won = {player.team: 0 for player in self.players}
        for lane in self.board.lanes:
            winner = lane.player_winning_lane()
            if winner is not None:
                lanes_won[winner] += 1
        for player in self.players:
            if lanes_won[player.team] > 1:
                return player.team
        return None

    def all_cards_played(self):
        return all(len(player.deck.cards) + len(player.hand.cards) == 0 for player in self.players)

    def find_side(self, side_id):
        for lane in self.board.lanes:
            for side in lane.sides:
                if side.side_id == side_id:
                    return side
        return None

    def new_turn(self):
        self.active_player().end_turn()
        self.active_player_index = (self.active_player_index + 1) % 2
        self.active_player().start_turn()

    def to_json(self, team):
        player = self.player_by_team(team)
        return {
            'active_player_index': self.active_player_index,
            'graveyard': self.graveyard.to_json(player),
            'players': [player.to_json(player) for player in self.players],
            'board': self.board.to_json(player),
            'winner': self.winner,
        }

