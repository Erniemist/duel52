from Board.Lane.Side.Minion.ClientMinion import ClientMinion
from Server.ServerCard import ServerCard


class ClientCard(ServerCard):
    def __init__(self, value: str, host, card_id, game, minion=None):
        self.card_id = card_id
        self.value = value
        self.host = host
        self.game = game
        self.minion = ClientMinion.from_json(card=self, side=host, game=game, data=minion) if minion else None

    def can_select(self, my_turn):
        return my_turn and self.game.active_player().team == self.host.player.team and self.game.active_player().actions > 0

    def on_select(self, cursor):
        cursor.pick_up(self)

    @staticmethod
    def from_json(host, game, data):
        value = data['value'] if 'value' in data.keys() else ''
        minion = data['minion'] if 'minion' in data.keys() else None

        return ClientCard(
            value=value,
            host=host,
            card_id=data['card_id'],
            game=game,
            minion=minion,
        )
