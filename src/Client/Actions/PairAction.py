from Client.Actions.Action import Action


class PairAction(Action):
    name = 'pair'

    def __init__(self, minion_1, minion_2):
        self.minion_1 = minion_1
        self.minion_2 = minion_2
        super().__init__()

    def data(self):
        return {'card_1': self.minion_1.card.card_id, 'card_2': self.minion_2.card.card_id}
