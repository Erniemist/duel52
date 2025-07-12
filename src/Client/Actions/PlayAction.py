from Client.Actions.Action import Action


class PlayAction(Action):
    name = 'play'

    def __init__(self, card, side):
        self.card = card
        self.side = side
        super().__init__()

    def data(self):
        return {'card': self.card.card_id, 'side': self.side.side_id}
