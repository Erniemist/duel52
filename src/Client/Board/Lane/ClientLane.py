from typing import Generator, Any
from Client.Card.ClientCard import ClientCard


class ClientLane:
    def __init__(self, game):
        self.game = game
        self.sides = []

    def get_cards(self) -> Generator[ClientCard, Any, None]:
        return (card for side in self.sides for card in side.cards)
