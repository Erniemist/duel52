import uuid


class ServerApp:
    def __init__(self, game, name):
        self.name = name
        self.game_id = str(uuid.uuid4().int)
        self.game = game
        self.teams = {}

    def add_connection(self, connection, team):
        connection.app = self
        self.teams[connection] = team

    def to_json(self, connection):
        return self.game.to_json(self.teams[connection])
