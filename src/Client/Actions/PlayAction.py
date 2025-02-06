from Client.Actions.Action import Action


class PlayAction(Action):
    name = 'play'

    def __init__(self, card_id, side_id):
        self.card_id = card_id
        self.side_id = side_id
        super().__init__()

    def data(self):
        return {'card': self.card_id, 'side': self.side_id}

    def resolve(self, game):
        game.active_player().play_card(
            card=game.find_card_from_hand(self.card_id),
            side=game.find_side(self.side_id),
        )
