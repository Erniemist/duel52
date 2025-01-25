from Board.Board import Board
from Cursor.Cursor import Cursor
from Graveyard.Graveyard import Graveyard
from Player.Player import Player


class GameState:
    def __init__(self):
        self.graveyard = Graveyard(self)
        self.players = [Player(team, self) for team in Player.TEAMS]
        self.board = Board(self)
        self.cursor = Cursor(self)
        self.active_player_index = 0
        self.active_player().start_turn(actions=2)
        self.turns = 0

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
