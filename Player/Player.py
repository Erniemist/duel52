from Deck.Deck import Deck
from Hand.Hand import Hand
from Player.PlayerView import PlayerView


class Player:
    US = 0
    THEM = 1
    TEAMS = [US, THEM]

    def __init__(self, team, game):
        self.team = team
        self.game = game
        self.hand = Hand(self, game)
        self.deck = Deck(self, game)
        self.actions = 0
        for i in range(5):
            self.deck.draw_from_top()

    def start_turn(self, actions=3):
        self.actions = actions
        self.deck.draw_from_top()

    def end_turn(self):
        for minion in self.minions():
            minion.end_turn()

    def minions(self):
        return [card.minion for side in self.sides() for card in side.cards]

    def sides(self):
        return [side for lane in self.game.board.lanes for side in lane.sides if side.team == self.team]

    def action(self):
        if self.actions < 1:
            raise Exception("Tried to take action with actions left")
        self.actions -= 1

    def play_card(self, side, card):
        self.action()
        card.move_to(side)

    def flip_card(self, minion):
        self.action()
        minion.face_down = False

    def pair_cards(self, minion, second_minion):
        if minion.team != self.team or second_minion.team != self.team:
            raise Exception("Tried to pair minion from the other team")
        if minion.value != second_minion.value:
            raise Exception("Can't pair non-matching minions")
        if minion.pair or second_minion.pair:
            raise Exception("Can't pair already paired minions")
        if minion.face_down or second_minion.face_down:
            raise Exception("Can't pair facedown minions")
        self.action()
        minion.pair = second_minion
        second_minion.pair = minion

    def attack(self, friendly_minion, enemy_minion):
        if friendly_minion.team != self.team:
            raise Exception("Tried to attack from an enemy minion")
        if enemy_minion.team == self.team:
            raise Exception("Tried to attack a friendly minion")
        if friendly_minion.attacks_left() < 1:
            raise Exception("Tried to attack with an exhausted minion")
        self.action()
        friendly_minion.attack(enemy_minion)
