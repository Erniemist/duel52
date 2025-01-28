from Board.Lane.Side.Minion.Minion import Minion


class Card:
    def __init__(self, value: str, host, card_id, game):
        self.card_id = card_id
        self.value = value
        self.host = host
        self.game = game
        self.minion = None

    def can_select(self, my_turn):
        return my_turn and self.game.active_player().team == self.host.team and self.game.active_player().actions > 0

    def on_select(self, cursor):
        cursor.pick_up(self)

    def move_to(self, new_host):
        self.host.remove_card(self)
        self.host = new_host
        new_host.add_card(self)

    def to_json(self):
        data = {
            'card_id': self.card_id,
            'value': self.value,
        }
        if self.minion:
            data['minion'] = self.minion.to_json()
        return data

    @staticmethod
    def from_json(host, game, data):
        card = Card(data['value'], host, data['card_id'], game)
        if 'minion' in data.keys():
            card.minion = Minion.from_json(card=card, side=host, game=game, data=data['minion'])
        return card
