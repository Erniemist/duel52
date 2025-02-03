from Server.ServerLane import ServerLane
from Server.ServerCard import ServerCard
from Server.ServerPlayer import ServerPlayer

from typing import TYPE_CHECKING, Generator, Any

if TYPE_CHECKING:
    from Server.ServerGameState import ServerGameState


class ServerBoard:
    num_lanes = 3

    def __init__(self, game, players):
        self.game: ServerGameState = game
        players: list[ServerPlayer]
        self.lanes = [ServerLane(game, players=players, lane_id=i) for i in range(self.num_lanes)]

    def get_cards(self) -> Generator[ServerCard, Any, None]:
        return (card for lane in self.lanes for card in lane.get_cards())

    def to_json(self, for_player: ServerPlayer) -> dict:
        return {'lanes': [lane.to_json(for_player) for lane in self.lanes]}

    @staticmethod
    def from_json(game, players, data):
        board = ServerBoard(game=game, players=players)
        for i, lane_data in enumerate(data['lanes']):
            lane = board.lanes[i]
            for j, side_data in enumerate(lane_data['sides']):
                side = lane.sides[j]
                for card_data in side_data['cards']:
                    side.cards.append(ServerCard.from_json(game, side, card_data))
        return board
