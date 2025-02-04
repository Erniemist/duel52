from Client.Board.ClientBoard import ClientBoard
from Client.ClientGameState import ClientGameState
from DataTransfer.GraveyardData import GraveyardData
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
        self.is_server = None

    @staticmethod
    def from_json(data):
        return GameData(
            active_player_index=data['active_player_index'],
            graveyard=GraveyardData.from_json(data['graveyard']),
            players=[PlayerData.from_json(player) for player in data['players']],
            board=data['board'],
            winner=data['winner'],
        )

    def make_server(self):
        self.is_server = True
        return ServerGameState(self)

    @staticmethod
    def from_server(server: ServerGameState, team):
        for_player = server.player_by_team(team)
        return GameData(
            active_player_index=server.active_player_index,
            graveyard=GraveyardData.from_server(server.graveyard, for_player=for_player),
            players=[PlayerData.from_server(player, for_player) for player in server.players],
            board=server.board.to_json(for_player=for_player),
            winner=server.winner.team if server.winner else None
        )

    def make_client(self):
        self.is_server = False
        return ClientGameState(self)

    def build(self, game):
        assert self.is_server is not None
        board = ServerBoard if self.is_server else ClientBoard
        players = [player_data.make(game, self.is_server) for player_data in self.players]
        return (
            self.graveyard.make(game, self.is_server),
            players,
            board.from_json(game, players, self.board),
        )

    def to_json(self):
        return {
            'active_player_index': self.active_player_index,
            'graveyard': self.graveyard.to_json(),
            'players': [player.to_json() for player in self.players],
            'board': self.board,
            'winner': self.winner
        }
