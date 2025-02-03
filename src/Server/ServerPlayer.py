from Client.Deck.Deck import Deck
from Client.Hand.Hand import Hand

from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from Server.ServerGameState import ServerGameState


class ServerPlayer:
    TEAMS = ['A', 'B']

    def __init__(self, team: str, game):
        self.team = team
        self.game: ServerGameState = game
        self.hand = Hand(game, self)
        self.deck = Deck(game, self)
        self.actions = 0
        self.known_cards: list[str] = []

    def start_turn(self, actions: int = 3):
        self.actions = actions
        self.deck.draw_from_top(self.hand)

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
        self.game.check_victory()
        if self.actions == 0 or self.no_possible_actions():
            self.actions = 0
            self.game.new_turn()

    def no_possible_actions(self):
        return len(self.hand.cards) == 0 and len([minion for minion in self.minions() if minion.could_act()]) == 0

    def play_card(self, side, card):
        self.take_action(lambda: card.move_to(side))

    def flip_minion(self, minion):
        self.take_action(lambda: minion.flip_up())

    def attack(self, friendly_minion, enemy_minion):
        if friendly_minion.team != self.team:
            raise Exception("Tried to attack from an enemy minion")
        if enemy_minion.team == self.team:
            raise Exception("Tried to attack a friendly minion")
        if friendly_minion.attacks_left() < 1:
            raise Exception("Tried to attack with an exhausted minion")
        self.take_action(lambda: friendly_minion.attack(enemy_minion))

    def pair_minions(self, minion, second_minion):
        if minion.team != self.team or second_minion.team != self.team:
            raise Exception("Tried to pair minion from the other team")
        if minion.value != second_minion.value:
            raise Exception("Can't pair non-matching minions")
        if minion.pair or second_minion.pair:
            raise Exception("Can't pair already paired minions")
        if minion.face_down or second_minion.face_down:
            raise Exception("Can't pair facedown minions")
        self.take_action(lambda: minion.pair_with(second_minion))

    def take_action(self, action):
        self.start_action()
        action()
        self.finish_action()

    def other_team(self):
        return next(team for team in self.TEAMS if team is not self.team)

    def other_player(self):
        return self.game.player_by_team(self.other_team())

    def learn(self, card):
        self.known_cards.append(card.card_id)

    def knows(self, card):
        return card.card_id in self.known_cards

    @staticmethod
    def from_json(game, data):
        player = ServerPlayer(data['team'], game)
        player.hand = Hand.from_json_server(game=game, player=player, data=data['hand'])
        player.known_cards = data['known_cards']
        player.deck = Deck.from_json_server(game=game, player=player, data=data['deck'])
        player.actions = data['actions']
        return player

    def to_json(self, for_player: Self):
        return {
            'hand': self.hand.to_json(for_player),
            'deck': self.deck.to_json(for_player),
            'actions': self.actions,
            'team': self.team,
            'known_cards': self.known_cards,
        }
