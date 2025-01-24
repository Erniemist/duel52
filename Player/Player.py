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
        for minion in self.minions():
            minion.start_turn()

    def view(self):
        return PlayerView(self)

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

    def attack(self, friendly_minion, enemy_minion):
        if friendly_minion.team != self.team:
            raise Exception("Tried to attack from an enemy minion")
        if enemy_minion.team == self.team:
            raise Exception("Tried to attack a friendly minion")
        if friendly_minion.attacks_left < 1:
            raise Exception("Tried to attack with an exhausted minion")
        self.action()
        friendly_minion.attack(enemy_minion)
