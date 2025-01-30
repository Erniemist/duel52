from Card.ClientCard import ClientCard
from Server.ServerMinion import ServerMinion


class Side:
    def __init__(self, game, lane, side_id, player):
        self.game = game
        self.lane = lane
        self.side_id = side_id
        self.player = player
        self.team = player.team
        self.cards = []

    def can_place(self, card, my_turn):
        return my_turn and self.team == self.game.active_player().team and self.player.actions > 0

    def on_place(self, card):
        self.game.play_event(card, self)

    def add_card(self, card):
        card.minion = ServerMinion(card, self, self.game)
        self.cards.append(card)

    def remove_card(self, card):
        card.minion = None
        self.cards = [c for c in self.cards if c is not card]

    def to_json(self, player):
        return {'cards': [card.to_json(player) for card in self.cards]}

    @staticmethod
    def from_json(lane, player, side_id, game, data):
        side = Side(game=game, lane=lane, side_id=side_id, player=player)
        for card_data in data['cards']:
            side.cards.append(ClientCard.from_json(host=side, game=game, data=card_data))
        return side
