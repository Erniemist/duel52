from Client.Actions.Action import Action


class ChooseAction(Action):
    name = 'choose'

    def __init__(self, card_id):
        self.card_id = card_id
        super().__init__()

    def data(self):
        return {'card': self.card_id}
