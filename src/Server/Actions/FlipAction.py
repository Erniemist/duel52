class FlipAction:
    name = 'flip'

    def __init__(self, game, card_id):
        self.player = game.active_player()
        self.minion = game.find_card_from_board(card_id).minion

    def resolve(self):
        self.validate()
        self.minion.flip_up()

    def validate(self):
        if self.minion not in self.player.minions():
            raise Exception(f"Minion {self.minion.card.card_id} is not on your board")
        if self.minion.frozen:
            raise Exception(f"Frozen minion {self.minion.card.card_id} cannot flip")
        if not self.minion.face_down:
            raise Exception(f"Faceup minion {self.minion.card.card_id} cannot flip")
