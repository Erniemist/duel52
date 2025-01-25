from Board.Board import Board
from Deck.Deck import Deck
from Graveyard.Graveyard import Graveyard
from Player.Player import Player


class GameState:
    def __init__(self):
        self.graveyard = Graveyard(self)
        self.players = self.make_players()
        self.board = Board(self)
        self.active_player_index = 0
        self.active_player().start_turn(actions=2)
        self.turns = 0

    def make_players(self):
        main_deck = Deck(self)
        players = []
        for team in Player.TEAMS:
            deck = Deck(self, [])
            for i in range(20):
                main_deck.draw_from_top(deck)
            players.append(Player(team, self, deck))
        return players

    def update(self):
        if self.active_player().actions == 0:
            self.new_turn()

    def active_player(self):
        return self.players[self.active_player_index]

    def new_turn(self):
        self.turns += 1
        self.active_player().end_turn()
        self.active_player_index = (self.active_player_index + 1) % 2
        self.active_player().start_turn()
