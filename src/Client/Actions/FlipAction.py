from Client.Actions.Action import Action


class FlipAction(Action):
    name = 'flip'

    def __init__(self, minion):
        self.minion = minion
        super().__init__()

    def data(self):
        return {'card': self.minion.card.card_id}
