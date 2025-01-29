class ServerCard:
    def __init__(self, value: str, host, card_id, game):
        self.card_id = card_id
        self.value = value
        self.host = host
        self.player = host.player
        self.game = game
        self.minion = None

    def move_to(self, new_host):
        self.host.remove_card(self)
        self.host = new_host
        new_host.add_card(self)

    def to_json(self, player):
        data = {'card_id': self.card_id}
        if player.knows(self):
            data['value'] = self.value
        if self.minion:
            data['minion'] = self.minion.to_json()
        return data
