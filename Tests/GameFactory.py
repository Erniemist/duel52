from DataTransfer.GameData import GameData


class GameFactory:
    def __init__(self):
        self.active_team = 'A'
        self.winner = None
        self.graveyard = []
        self.board = []
        self.players = []

    def build(self):
        active_team_index = 0
        players = self.players
        return GameData(
            self.winner,
            active_team_index,
            self.graveyard,
            players,
            self.board,
        )

