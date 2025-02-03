from Client.Deck.Deck import Deck
from Client.Hand.Hand import Hand
from Client.Player.ClientPlayer import ClientPlayer
from Server.ServerPlayer import ServerPlayer


class PlayerData:
    def __init__(self, hand, deck, actions, team, known_cards):
        self.actions = actions
        self.team = team
        self.known_cards = known_cards
        self.hand = hand
        self.deck = deck

    @staticmethod
    def from_json(data):
        return PlayerData(
            hand=data['hand'],
            deck=data['deck'],
            actions=data['actions'],
            team=data['team'],
            known_cards=data['known_cards'],
        )

    def make_server(self, game):
        return ServerPlayer(self.team, game, self)

    def build_for_server(self, game, player):
        return (
            Hand.from_json_server(game, player, self.hand),
            Deck.from_json_server(game, player, self.deck),
        )

    @staticmethod
    def from_server(player: ServerPlayer, for_player):
        return PlayerData(
            actions=player.actions,
            team=player.team,
            known_cards=player.known_cards,
            hand=player.hand.to_json(for_player),
            deck=player.deck.to_json(for_player),
        )

    def make_client(self, game):
        return ClientPlayer(game, self)

    def build_for_client(self, game, player):
        return (
            Hand.from_json(game, player, self.hand),
            Deck.from_json(game, player, self.deck),
        )

    def to_json(self):
        return {
            'actions': self.actions,
            'team': self.team,
            'known_cards': self.known_cards,
            'hand': self.hand,
            'deck': self.deck,
        }
