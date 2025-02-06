class AttackAction:
    name = 'attack'

    def __init__(self, game, card_1_id, card_2_id):
        self.player = game.active_player()
        self.friendly_minion = game.find_card_from_board(card_1_id).minion
        self.enemy_minion = game.find_card_from_board(card_2_id).minion

    def resolve(self):
        self.validate()
        self.friendly_minion.attack(self.enemy_minion)

    def validate(self):
        if self.friendly_minion.frozen:
            raise Exception(f"Frozen minion {self.friendly_minion.card.card_id} cannot attack")
        if self.friendly_minion.team != self.player.team:
            raise Exception("Tried to attack from an enemy minion")
        if self.enemy_minion.team == self.player.team:
            raise Exception("Tried to attack a friendly minion")
        if self.friendly_minion.attacks_left() < 1:
            raise Exception("Tried to attack with an exhausted minion")
