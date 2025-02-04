import uuid


class Action:
    def __init__(self, name, data):
        self.action_id = str(uuid.uuid4().int)
        self.name = name
        self.data = data
        self.sent = False
        self.resolved = False

    def json(self):
        return {'action': self.name, 'data': self.data, 'action_id': self.action_id}

    @staticmethod
    def play(card, side):
        return Action('play', {'card': card, 'side': side})

    @staticmethod
    def flip(card):
        return Action('flip', {'card': card})

    @staticmethod
    def attack(card_1, card_2):
        return Action('attack', {'card_1': card_1, 'card_2': card_2})

    @staticmethod
    def pair(card_1, card_2):
        return Action('pair', {'card_1': card_1, 'card_2': card_2})
