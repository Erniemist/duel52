from Board.Board import Board
from Server.ServerLane import ServerLane


class ServerBoard(Board):
    num_lanes = 3

    def __init__(self, game, players):
        super().__init__(game, [ServerLane(game, players=players, lane_id=i) for i in range(self.num_lanes)])

    def to_json(self, player):
        return {'lanes': [lane.to_json(player) for lane in self.lanes]}
