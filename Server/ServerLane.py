from Server.ServerSide import ServerSide
from Server.ServerCard import ServerCard

from typing import TYPE_CHECKING, Generator, Any

if TYPE_CHECKING:
    from Server.ServerGameState import ServerGameState
    from Server.ServerPlayer import ServerPlayer


class ServerLane:
    def __init__(self, game, players, lane_id: int):
        self.game: ServerGameState = game
        self.players: list[ServerPlayer] = players
        self.lane_id = lane_id
        self.sides: list[ServerSide] = [
            ServerSide(game, self, side_id=lane_id * 2 + i, player=player)
            for i, player in enumerate(players)
        ]

    def player_winning_lane(self):
        if len(self.sides[0].cards) == 0 and len(self.sides[1].cards) > 0:
            return self.sides[1].player
        if len(self.sides[1].cards) == 0 and len(self.sides[0].cards) > 0:
            return self.sides[0].player
        return None

    def get_cards(self) -> Generator[ServerCard, Any, None]:
        return (card for side in self.sides for card in side.cards)

    def to_json(self, for_player):
        return {'sides': [side.to_json(for_player) for side in self.sides]}
