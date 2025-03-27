from Client.Board.Lane.Side.Minion.Minion import Minion
from Server.Triggers.AttackTrigger import AttackTrigger
from Server.Triggers.FlipTrigger import FlipTrigger


class ServerMinion(Minion):
    base_max_attacks = 1

    def __init__(self, card, game, minion_data=None):
        self.card = card
        self.game = game
        self.value = card.value
        self.player = self.side.player
        self.team = self.player.team
        self.pair = None
        if minion_data is None:

            self.max_hp = self.card.type.max_hp if self.card.type else 2
            self.hp = self.max_hp
            self.face_down = True
            self.attacks_made = 0
            self.max_attacks = self.base_max_attacks
            self.frozen = False
        else:
            self.max_hp = minion_data.max_hp
            self.hp = minion_data.hp
            self.face_down = minion_data.face_down
            self.attacks_made = minion_data.attacks_made
            self.max_attacks = minion_data.max_attacks
            self.frozen = minion_data.frozen

    @property
    def side(self):
        return self.card.host

    def end_turn(self):
        self.attacks_made = 0
        self.max_attacks = self.base_max_attacks
        self.frozen = False

    def flip_up(self):
        if not self.face_down:
            return
        self.face_down = False
        self.game.trigger(FlipTrigger(self.card.card_id, self.player))
        self.player.other_player().learn(self.card)

    def attack(self, enemies):
        self.attacks_made += 1
        damage = 2 if self.pair else 1
        for enemy in enemies:
            self.game.trigger(AttackTrigger(
                attacker_id=self.card.card_id,
                defender_id=enemy.card.card_id,
                player=self.player,
            ))
            enemy.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        if self.pair:
            self.pair.pair = None
        self.card.move_to(self.game.graveyard)

    def could_pair(self):
        return self.pair is None and self.value in [
            other.value
            for other in self.side.cards
            if other.minion is not self and other.minion.pair is None
        ]

    def could_attack(self):
        return self.attacks_left() > 0 and len([
            enemy
            for enemy in self.player.other_player().minions()
            if enemy.side.lane is self.side.lane
        ]) > 0

    def could_act(self):
        return self.could_attack() or self.face_down or self.could_pair()

    def has_active_keyword(self, keyword):
        return not self.face_down and self.card.has_keyword(keyword)
