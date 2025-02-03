from Client.Board.Lane.Side.Minion.Minion import Minion


class ServerMinion(Minion):
    def __init__(self, card, side, game):
        self.card = card
        self.value = card.value
        self.side = side
        self.player = side.player
        self.team = self.player.team
        self.game = game
        self.hp = self.max_hp
        self.face_down = True
        self.pair = None
        self.attacks_made = 0

    def end_turn(self):
        self.attacks_made = 0

    def flip_up(self):
        self.face_down = False
        self.player.other_player().learn(self.card)

    def attack(self, enemy):
        self.attacks_made += 1
        damage = 2 if self.pair else 1
        enemy.hp -= damage
        if enemy.hp <= 0:
            enemy.die()

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
            if enemy.side == self.side
        ]) > 0

    def could_act(self):
        return self.could_attack() or self.face_down or self.could_pair()

    def to_json(self) -> dict:
        data = {
            'hp': self.hp,
            'face_down': self.face_down,
            'attacks_made': self.attacks_made,
        }
        if self.pair:
            data['pair'] = self.pair.card.card_id
        return data
