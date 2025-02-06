class PlayAction:
    name = 'play'

    def __init__(self, game, card_id, side_id):
        self.player = game.active_player()
        self.card = game.find_card_from_hand(card_id)
        self.side = game.find_side(side_id)

    def resolve(self):
        self.card.move_to(self.side)
