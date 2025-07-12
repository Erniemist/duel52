class PairAction:
    name = 'pair'

    def __init__(self, game, card_1_id, card_2_id):
        self.player = game.active_player()
        self.minion_1 = game.find_card_from_board(card_1_id).minion
        self.minion_2 = game.find_card_from_board(card_2_id).minion
        super().__init__()

    def resolve(self):
        self.validate()
        self.minion_1.pair_with(self.minion_2)

    def validate(self):
        if self.minion_1.frozen:
            raise Exception(f"Frozen minion {self.minion_1.card.card_id} cannot pair")
        if self.minion_2.frozen:
            raise Exception(f"Frozen minion {self.minion_2.card.card_id} cannot pair")
        if self.minion_1.team != self.player.team or self.minion_2.team != self.player.team:
            raise Exception("Tried to pair minion from the other team")
        if self.minion_1.value != self.minion_2.value:
            raise Exception("Can't pair non-matching minions")
        if self.minion_1.pair or self.minion_2.pair:
            raise Exception("Can't pair already paired minions")
        if self.minion_1.face_down or self.minion_2.face_down:
            raise Exception("Can't pair facedown minions")
