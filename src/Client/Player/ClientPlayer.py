from Client.Deck.Deck import Deck
from Client.Hand.Hand import Hand


class ClientPlayer:
    def __init__(self, game, player_data):
        self.game = game
        hand, deck = player_data.build(game, self)
        self.team = player_data.team
        self.hand: Hand = hand
        self.deck: Deck = deck
        self.actions = player_data.actions
        self.known_cards = player_data.known_cards
