from typing import TYPE_CHECKING

from Server.ServerCard import ServerCard
from Server.ServerMinion import ServerMinion
from Server.Triggers.DeathTrigger import DeathTrigger

if TYPE_CHECKING:
    from Server.ServerLane import ServerLane
    from Server.ServerGameState import ServerGameState
    from Server.ServerPlayer import ServerPlayer


class ServerSide:
    def __init__(self, game, lane, side_id, player):
        self.game: ServerGameState = game
        self.lane: ServerLane = lane
        self.side_id = side_id
        self.player: ServerPlayer = player
        self.team = player.team
        self.cards: list[ServerCard] = []

    def add_card(self, card: ServerCard):
        self.cards.append(card)
        if card.minion:
            pair = card.minion.pair
            if not pair or pair.card.host is self:
                return
            pair.card.move_to(self)
            return
        card.minion = ServerMinion(card, self.game)

    def remove_card(self, card):
        self.cards.remove(card)
        if self.still_on_board(card):
            return
        card.minion = None
        if card.host is self.game.graveyard:
            self.game.trigger(DeathTrigger(card.card_id, self.player))

    def still_on_board(self, card):
        return any(card.host is side for lane in self.game.board.lanes for side in lane.sides)

    def other_side(self):
        return next(side for side in self.lane.sides if side.side_id != self.side_id)

    def minions(self):
        return [card.minion for card in self.cards]
