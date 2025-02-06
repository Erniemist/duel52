class FlipAction:
    name = 'flip'

    def __init__(self, game, card_id):
        self.player = game.active_player()
        self.minion = game.find_card_from_board(card_id).minion

    def resolve(self):
        self.validate()
        self.player.flip_minion(self.minion)

    def validate(self):
        if self.minion.frozen:
            raise Exception(f"Frozen minion {self.minion.card.card_id} cannot flip")
