from Deck.Deck import Deck
from Hand.Hand import Hand


class ClientPlayer:
    def __init__(self, team, game, deck, hand, actions):
        self.team = team
        self.game = game
        self.hand = Hand.from_json(game=game, data=hand)
        self.deck = Deck.from_json(game=game, data=deck)
        self.actions = actions

    @staticmethod
    def from_json(game, data):
        return ClientPlayer(
            team=data['team'],
            game=game,
            deck=data['deck'],
            hand=data['hand'],
            actions=data['actions'],
        )
