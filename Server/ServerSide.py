from typing import TYPE_CHECKING

from Server.ServerCard import ServerCard
from Server.ServerMinion import ServerMinion
from Triggers.DeathTrigger import DeathTrigger

if TYPE_CHECKING:
    from Server.ServerLane import ServerLane
    from Server.ServerGameState import ServerGameState
    from Server.ServerPlayer import ServerPlayer


class ServerSide:
    def __init__(self, game, lane, side_id: int, player):
        self.game: ServerGameState = game
        self.lane: ServerLane = lane
        self.side_id = side_id
        self.player: ServerPlayer = player
        self.team = player.team
        self.cards: list[ServerCard] = []

    def add_card(self, card: ServerCard):
        card.minion = ServerMinion(card, self, self.game)
        self.cards.append(card)

    def remove_card(self, card):
        card.minion_last_info = card.minion
        card.minion = None
        if card.host is self.game.graveyard:
            self.game.trigger(DeathTrigger(card.card_id))
        self.cards = [c for c in self.cards if c is not card]

    def to_json(self, for_player):
        return {'cards': [card.to_json(for_player) for card in self.cards]}
