from Deck.Deck import Deck
from Hand.Hand import Hand
from Server.ServerPlayer import ServerPlayer


class ClientPlayer:
    def __init__(self, team, game, deck, hand, actions):
        self.team = team
        self.game = game
        self.hand = Hand.from_json(game=game, player=self, data=hand)
        self.deck = Deck.from_json(game=game, player=self, data=deck)
        self.actions = actions
        self.known_cards = []

    def play_card(self, side, card):
        card.move_to(side)

    def flip_minion(self, minion):
        minion.flip_up()

    def attack(self, friendly_minion, enemy_minion):
        friendly_minion.attack(enemy_minion)

    def pair_minions(self, minion, second_minion):
        minion.pair_with(second_minion)

    @staticmethod
    def from_json(game, data):
        return ClientPlayer(
            team=data['team'],
            game=game,
            deck=data['deck'],
            hand=data['hand'],
            actions=data['actions'],
        )
