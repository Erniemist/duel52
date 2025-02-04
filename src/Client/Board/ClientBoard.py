from typing import Generator, Any
from Client.Card.ClientCard import ClientCard


class ClientBoard:
    def __init__(self, game, players, board_data):
        self.game = game
        self.lanes = board_data.build(game, players)

    def get_cards(self) -> Generator[ClientCard, Any, None]:
        return (card for lane in self.lanes for card in lane.get_cards())
