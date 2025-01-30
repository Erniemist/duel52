from Card.CardTypes.Three import Three


class ServerCard:
    types = {
        Three.value: Three,
    }

    def __init__(self, value: str, host, card_id, game):
        self.card_id = card_id
        self.value = value
        if value in self.types:
            self.type = self.types[value](self)
        else:
            self.type = None
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
