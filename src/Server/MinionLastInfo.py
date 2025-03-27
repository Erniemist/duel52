from Server.ServerMinion import ServerMinion


class MinionLastInfo:
    def __init__(self, minion: ServerMinion):
        self.side = minion.side
        self.face_down = minion.face_down
        self.team = minion.team
