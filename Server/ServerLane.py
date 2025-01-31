from Board.Lane.Lane import Lane
from Server.ServerSide import ServerSide


class ServerLane(Lane):
    def __init__(self, game, players, lane_id):
        super().__init__(game, players, lane_id, [
            ServerSide(game, self, side_id=lane_id * 2 + i, player=player)
            for i, player in enumerate(players)
        ])

    def player_winning_lane(self):
        if len(self.sides[0].cards) == 0 and len(self.sides[1].cards) > 0:
            return self.sides[1].team
        if len(self.sides[1].cards) == 0 and len(self.sides[0].cards) > 0:
            return self.sides[0].team
        return None

    def to_json(self, player):
        return {'sides': [side.to_json(player) for side in self.sides]}
