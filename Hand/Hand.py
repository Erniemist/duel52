from Card.Card import Card


class Hand:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.team = player.team
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]

    def to_json(self):
        return {
            'cards': [card.to_json() for card in self.cards]
        }

    @staticmethod
    def from_json(player, game, data):
        hand = Hand(player=player, game=game)
        hand.cards = [Card.from_json(host=hand, game=game, data=card_data) for card_data in data['cards']]
        return hand