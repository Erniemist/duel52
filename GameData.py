from Board.ClientBoard import ClientBoard
from ClientGameState import ClientGameState
from Graveyard.Graveyard import Graveyard
from Player.ClientPlayer import ClientPlayer
from Server.ServerBoard import ServerBoard
from Server.ServerGameState import ServerGameState
from Server.ServerPlayer import ServerPlayer


class GameData:
    def __init__(self, winner, active_player_index, graveyard, players, board):
        self.winner = winner
        self.active_player_index = active_player_index
        self.graveyard = graveyard
        self.players = players
        self.board = board

    @staticmethod
    def from_json(data):
        return GameData(
            active_player_index=data['active_player_index'],
            graveyard=data['graveyard'],
            players=data['players'],
            board=data['board'],
            winner=data['winner'],
        )

    def make_server(self):
        return ServerGameState(self)

    def build_for_server(self, game):
        players = [ServerPlayer.from_json(game, player_data) for player_data in self.players]
        return (
            Graveyard.from_json(game, self.graveyard),
            players,
            ServerBoard.from_json(game, players, self.board),
        )

    @staticmethod
    def from_server(server: ServerGameState, team):
        for_player = server.player_by_team(team)
        return GameData(
            active_player_index=server.active_player_index,
            graveyard=server.graveyard.to_json(for_player=for_player),
            players=[player.to_json(for_player=for_player) for player in server.players],
            board=server.board.to_json(for_player=for_player),
            winner=server.winner.team if server.winner else None
        )

    def make_client(self, app):
        return ClientGameState(self, app)

    def build_for_client(self, game):
        players = [ClientPlayer.from_json(game, player_data) for player_data in self.players]
        return (
            Graveyard.from_json(game, self.graveyard),
            players,
            ClientBoard.from_json(game, players, self.board),
        )

    def to_json(self):
        return {
            'active_player_index': self.active_player_index,
            'graveyard': self.graveyard,
            'players': self.players,
            'board': self.board,
            'winner': self.winner
        }
