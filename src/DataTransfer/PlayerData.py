from Client.Card.ClientCard import ClientCard
from Client.Deck.Deck import Deck
from Client.Hand.Hand import Hand
from Client.Player.ClientPlayer import ClientPlayer
from Server.ServerCard import ServerCard
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
            hand=data['hand'],
            deck=data['deck'],
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
            hand={'cards': [card.to_json(for_player) for card in player.hand.cards]},
            deck={'cards': [card.to_json(for_player) for card in player.deck.cards]},
        )

    def build(self, game, player):
        assert self.is_server is not None
        card = ServerCard if self.is_server else ClientCard
        hand = Hand(game, player)
        hand.cards = [card.from_json(host=hand, game=game, data=card_data) for card_data in self.hand['cards']]
        deck = Deck(game, player)
        deck.cards = [card.from_json(host=deck, game=game, data=card_data) for card_data in self.deck['cards']]
        return hand, deck

    def to_json(self):
        return {
            'actions': self.actions,
            'team': self.team,
            'known_cards': self.known_cards,
            'hand': self.hand,
            'deck': self.deck,
        }
