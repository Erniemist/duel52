import uuid

from Client.Board.ClientBoard import ClientBoard
from Client.Board.Lane.ClientLane import ClientLane
from Client.Board.Lane.Side.ClientSide import ClientSide
from Client.Card.ClientCard import ClientCard
from Server.ServerBoard import ServerBoard
from Server.ServerCard import ServerCard
from Server.ServerLane import ServerLane
from Server.ServerSide import ServerSide


class BoardData:
    def __init__(self, lanes):
        self.lanes = lanes
        self.is_server = None

    @staticmethod
    def from_json(data):
        return BoardData(lanes=data['lanes'])

    def make(self, game, players, is_server):
        self.is_server = is_server
        return ServerBoard(game, players, self) if is_server else ClientBoard(game, players, self)

    @staticmethod
    def from_server(board: ServerBoard, for_player):
        return BoardData(lanes=[
            {'sides': [
                {'cards': [card.to_json(for_player) for card in side.cards]}
                for side in lane.sides
            ]}
            for lane in board.lanes
        ])

    def build(self, game, players):
        assert self.is_server is not None
        lane = ServerLane if self.is_server else ClientLane

        lanes = []
        for i, lane_data in enumerate(self.lanes):
            lanes.append(self.build_lane(game, players, i, lane(game), lane_data['sides']))
        return lanes

    def build_lane(self, game, players, i, lane, sides_data):
        sides = []
        side = ServerSide if self.is_server else ClientSide
        for j, player, side_data in zip(range(len(players)), players, sides_data):
            side_obj = side(game, lane, i * 2 + j, player)
            for card_data in side_data['cards']:
                card = ServerCard if self.is_server else ClientCard
                side_obj.cards.append(card.from_json(host=side_obj, game=game, data=card_data))
            sides.append(side_obj)
        lane.sides = sides
        return lane

    def to_json(self):
        return {'lanes': self.lanes}
