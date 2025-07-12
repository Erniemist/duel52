class PlayAction:
    name = 'play'

    def __init__(self, game, card_id, side_id):
        self.player = game.active_player()
        self.card = game.find_card_from_hand(card_id)
        self.side = game.find_side(side_id)

    def resolve(self):
        self.validate()
        self.card.move_to(self.side)

    def validate(self):
        if self.side.team != self.player.team:
            raise Exception(f"Can't play card {self.card.card_id} to enemy side {self.side.side_id}")
        if not any(self.card.card_id == card.card_id for card in self.player.hand.cards):
            raise Exception(f"Card {self.card.card_id} is not in hand to play")
