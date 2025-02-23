from Server.ServerSide import ServerSide
from Server.ServerCard import ServerCard

from typing import TYPE_CHECKING, Generator, Any

if TYPE_CHECKING:
    from Server.ServerGameState import ServerGameState


class ServerLane:
    def __init__(self, game):
        self.game: ServerGameState = game
        self.sides: list[ServerSide] = []

    def player_winning_lane(self):
        if len(self.sides[0].cards) == 0 and len(self.sides[1].cards) > 0:
            return self.sides[1].player
        if len(self.sides[1].cards) == 0 and len(self.sides[0].cards) > 0:
            return self.sides[0].player
        return None

    def get_cards(self) -> Generator[ServerCard, Any, None]:
        return (card for side in self.sides for card in side.cards)
