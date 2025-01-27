from Board.Board import Board
from Deck.Deck import Deck
from Graveyard.Graveyard import Graveyard
from Player.Player import Player


class GameState:
    def __init__(self):
        self.message = None
        self.graveyard = None
        self.players = []
        self.board = None
        self.active_player_index = 0
        self.turns = 0

    def start_game(self):
        self.graveyard = Graveyard(self)
        self.players = self.make_players()
        self.board = Board(self)
        for player in self.players:
            player.start_game()
        self.active_player().start_turn(actions=2)

    def make_players(self):
        main_deck = Deck(self)
        players = []
        for team in Player.TEAMS:
            deck = Deck(self, [])
            for i in range(20):
                main_deck.draw_from_top(deck)
            players.append(Player(team, self, deck))
        return players

    def send_message(self, message):
        if self.message:
            pass
        self.message = message

    def update(self):
        if self.active_player().actions == 0:
            self.new_turn()
        message = self.message
        self.message = None
        return message

    def active_player(self):
        return self.players[self.active_player_index]

    def new_turn(self):
        self.send_message('New turn')
        self.turns += 1
        self.active_player().end_turn()
        self.active_player_index = (self.active_player_index + 1) % 2
        self.active_player().start_turn()

    def to_json(self):
        return {
            'active_player_index': self.active_player_index,
            'graveyard': self.graveyard.to_json(),
            'players': [player.to_json() for player in self.players],
            'board': self.board.to_json(),
            'turns': self.turns,
        }

    @staticmethod
    def from_json(data):
        game = GameState()
        game.active_player_index = data['active_player_index']
        game.turns = data['turns']
        game.graveyard = Graveyard.from_json(game=game, data=data['graveyard'])
        game.players = [Player.from_json(game=game, data=player_data) for player_data in data['players']]
        game.board = Board.from_json(game=game, data=data['board'])
        return game
