from Client.Actions.Action import Action


class AttackAction(Action):
    name = 'attack'

    def __init__(self, card_1_id, card_2_id):
        self.card_1_id = card_1_id
        self.card_2_id = card_2_id
        super().__init__()

    def data(self):
        return {'card_1': self.card_1_id, 'card_2': self.card_2_id}
