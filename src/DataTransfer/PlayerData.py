from Client.Deck.Deck import Deck
from Client.Hand.Hand import Hand
from Client.Player.ClientPlayer import ClientPlayer
from DataTransfer.CardData import CardData
from Server.ServerPlayer import ServerPlayer


class PlayerData:
    def __init__(self, hand, deck, actions, team, known_cards):
        self.actions = actions
        self.team = team
        self.known_cards = known_cards
        self.hand = hand
        self.deck = deck
        self.is_server = None

    @staticmethod
    def from_json(data):
        return PlayerData(
            hand=[CardData.from_json(card_data) for card_data in data['hand']['cards']],
            deck=[CardData.from_json(card_data) for card_data in data['deck']['cards']],
            actions=data['actions'],
            team=data['team'],
            known_cards=data['known_cards'],
        )

    def make(self, game, is_server):
        self.is_server = is_server
        return ServerPlayer(self.team, game, self) if is_server else ClientPlayer(game, self)

    @staticmethod
    def from_server(player: ServerPlayer, for_player):
        return PlayerData(
            actions=player.actions,
            team=player.team,
            known_cards=player.known_cards,
            hand=[CardData.from_server(card, for_player) for card in player.hand.cards],
            deck=[CardData.from_server(card, for_player) for card in player.deck.cards],
        )

    def build(self, game, player):
        assert self.is_server is not None
        hand = Hand(game, player)
        hand.cards = [card_data.make(game, hand, self.is_server) for card_data in self.hand]
        deck = Deck(game, player)
        deck.cards = [card_data.make(game, deck, self.is_server) for card_data in self.deck]
        return hand, deck

    def to_json(self):
        return {
            'actions': self.actions,
            'team': self.team,
            'known_cards': self.known_cards,
            'hand': {'cards': [card.to_json() for card in self.hand]},
            'deck': {'cards': [card.to_json() for card in self.deck]},
        }
