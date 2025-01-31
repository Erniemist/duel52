from Card.Card import Card
from Card.CardTypes.Three import Three


class ServerCard(Card):
    types = {
        Three.value: Three,
    }

    def __init__(self, value: str, host, card_id, game):
        if value in self.types:
            self.type = self.types[value](self)
        else:
            self.type = None
        super().__init__(value, host, card_id, game)
        self.minion = None

    def to_json(self, player):
        data = {'card_id': self.card_id}
        if player.knows(self):
            data['value'] = self.value
        if self.minion:
            data['minion'] = self.minion.to_json()
        return data
