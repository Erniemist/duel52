from Client.Deck.Deck import Deck
from Client.Hand.Hand import Hand

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Server.ServerGameState import ServerGameState


class ServerPlayer:
    TEAMS = ['A', 'B']

    def __init__(self, team, game, player_data=None):
        self.game: ServerGameState = game
        self.team = team
        if player_data is None:
            self.hand = Hand(game, self)
            self.deck = Deck(game, self)
            self.actions = 0
            self.known_cards: list[str] = []
        else:
            hand, deck = player_data.build(game, self)
            self.hand = hand
            self.deck = deck
            self.actions = player_data.actions
            self.known_cards: list[str] = player_data.known_cards

    def start_turn(self, actions: int = 3):
        self.actions = actions
        self.deck.draw_from_top(self.hand)
        if self.no_possible_actions():
            self.game.new_turn()

    def end_turn(self):
        for minion in self.minions():
            minion.end_turn()

    def minions(self):
        return (card.minion for side in self.sides() for card in side.cards)

    def sides(self):
        return [side for lane in self.game.board.lanes for side in lane.sides if side.team == self.team]

    def start_action(self):
        if self.actions < 1:
            raise Exception("Tried to take action with no actions left")

    def finish_action(self):
        self.actions -= 1

    def no_possible_actions(self):
        return len(self.hand.cards) == 0 and len([minion for minion in self.minions() if minion.could_act()]) == 0

    def other_team(self):
        return next(team for team in self.TEAMS if team is not self.team)

    def other_player(self):
        return self.game.player_by_team(self.other_team())

    def learn(self, card):
        self.known_cards.append(card.card_id)

    def knows(self, card):
        return card.card_id in self.known_cards
