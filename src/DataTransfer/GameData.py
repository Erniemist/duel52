from Client.Board.ClientBoard import ClientBoard
from Client.ClientGameState import ClientGameState
from Client.Graveyard.Graveyard import Graveyard
from DataTransfer.PlayerData import PlayerData
from Server.ServerBoard import ServerBoard
from Server.ServerGameState import ServerGameState


class GameData:
    def __init__(self, winner, active_player_index, graveyard, players, board):
        self.winner = winner
        self.active_player_index = active_player_index
        self.graveyard = graveyard
        self.players: list[PlayerData] = players
        self.board = board

    @staticmethod
    def from_json(data):
        return GameData(
            active_player_index=data['active_player_index'],
            graveyard=data['graveyard'],
            players=[PlayerData.from_json(player) for player in data['players']],
            board=data['board'],
            winner=data['winner'],
        )

    def make_server(self):
        return ServerGameState(self)

    def build_for_server(self, game):
        players = [player_data.make_server(game) for player_data in self.players]
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
            players=[PlayerData.from_server(player, for_player) for player in server.players],
            board=server.board.to_json(for_player=for_player),
            winner=server.winner.team if server.winner else None
        )

    def make_client(self):
        return ClientGameState(self)

    def build_for_client(self, game):
        players = [player_data.make_client(game) for player_data in self.players]
        return (
            Graveyard.from_json(game, self.graveyard),
            players,
            ClientBoard.from_json(game, players, self.board),
        )

    def to_json(self):
        return {
            'active_player_index': self.active_player_index,
            'graveyard': self.graveyard,
            'players': [player.to_json() for player in self.players],
            'board': self.board,
            'winner': self.winner
        }
