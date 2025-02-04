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
        self.game = None
        self.players = None

    @staticmethod
    def from_json(data):
        return BoardData(lanes=data['lanes'])

    def make(self, game, players, is_server):
        self.is_server = is_server
        self.game = game
        self.players = players
        return ServerBoard(game, players, self) if is_server else ClientBoard(game, self)

    @staticmethod
    def from_server(board: ServerBoard, for_player):
        return BoardData(lanes=[
            {'sides': [
                {
                    'side_id': side.side_id,
                    'cards': [card.to_json(for_player) for card in side.cards]
                } for side in lane.sides
            ]} for lane in board.lanes
        ])

    def build(self):
        assert self.is_server is not None
        lane = ServerLane if self.is_server else ClientLane

        lanes = []
        for lane_data in self.lanes:
            lanes.append(self.build_lane(lane(self.game), lane_data['sides']))
        return lanes

    def build_lane(self, lane, sides_data):
        sides = []
        side = ServerSide if self.is_server else ClientSide
        for player, side_data in zip(self.players, sides_data):
            sides.append(
                self.build_side(
                    side_data,
                    side(self.game, lane, side_data['side_id'], player),
                )
            )
        lane.sides = sides
        return lane

    def build_side(self, side_data, side):
        card = ServerCard if self.is_server else ClientCard
        for card_data in side_data['cards']:
            side.cards.append(card.from_json(host=side, game=self.game, data=card_data))
        return side

    def to_json(self):
        return {'lanes': self.lanes}
