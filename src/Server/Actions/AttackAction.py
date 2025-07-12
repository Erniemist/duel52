from Server.CardTypes.Abilities.Cleave import Cleave
from Server.CardTypes.Abilities.Jack import Jack
from Server.CardTypes.Abilities.Stealth import Stealth


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
        if len(self.enemy_minions) > 1:
            if not self.friendly_minion.has_active_keyword(Cleave):
                raise Exception("Tried to attack multiple minions")
            if any(minion.has_active_keyword(Stealth) for minion in self.enemy_minions):
                raise Exception("Tried to cleave a Stealth card")
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
        if any(enemy_minion.has_keyword(Jack) for enemy_minion in self.enemy_minions[0].side.cards):
            if any(enemy_minion.card.has_keyword(Jack) == False for enemy_minion in self.enemy_minions):
                raise Exception("Tried to attack a non-Jack minion")
