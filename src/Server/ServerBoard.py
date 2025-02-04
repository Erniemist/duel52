from Server.ServerLane import ServerLane
from Server.ServerCard import ServerCard

from typing import TYPE_CHECKING, Generator, Any

from Server.ServerSide import ServerSide

if TYPE_CHECKING:
    from Server.ServerGameState import ServerGameState


class ServerBoard:
    num_lanes = 3

    def __init__(self, game, players, board_data=None):
        self.game: ServerGameState = game
        if board_data is None:
            self.lanes = []
            for i in range(self.num_lanes):
                lane = ServerLane(game)
                sides = []
                for j, player in enumerate(players):
                    sides.append(ServerSide(game, lane, i * 2 + j, player))
                lane.sides = sides
                self.lanes.append(lane)
        else:
            self.lanes = board_data.build(game, players)

    def get_cards(self) -> Generator[ServerCard, Any, None]:
        return (card for lane in self.lanes for card in lane.get_cards())
