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
        self.hand = Hand(self)
        self.deck = Deck(self)
        self.actions = 0

    def start_turn(self):
        self.actions = 3

    def view(self):
        return PlayerView(self)
