from Server.CardTypes.Abilities.Ten import Ten


class AttackAction:
    name = 'attack'

    def __init__(self, game, attacker, targets):
        self.player = game.active_player()
        self.friendly_minion = game.find_card_from_board(attacker).minion
        self.enemy_minions = [game.find_card_from_board(target).minion for target in targets]

    def resolve(self):
        self.validate()
        self.friendly_minion.attack(self.enemy_minions)

    def validate(self):
        if len(self.enemy_minions) > 1 and not self.friendly_minion.card.has_keyword(Ten):
            raise Exception(f"Tried to attack multiple minions")
        if self.friendly_minion.frozen:
            raise Exception(f"Frozen minion {self.friendly_minion.card.card_id} cannot attack")
        if self.friendly_minion.team != self.player.team:
            raise Exception("Tried to attack from an enemy minion")
        if any(enemy_minion.team == self.player.team for enemy_minion in self.enemy_minions):
            raise Exception("Tried to attack a friendly minion")
        if any(enemy_minion.side.lane != self.friendly_minion.side.lane for enemy_minion in self.enemy_minions):
            raise Exception("Tried to attack a minion in another lane")
        if self.friendly_minion.attacks_left() < 1:
            raise Exception("Tried to attack with an exhausted minion")
        if self.friendly_minion.face_down:
            raise Exception("Tried to attack with a facedown minion")
