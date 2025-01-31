from Board.Lane.Side.Minion.Minion import Minion
from Triggers.DeathTrigger import DeathTrigger


class ServerMinion(Minion):
    def __init__(self, card, side, game):
        super().__init__(card, side, game, hp=self.max_hp, face_down=True, attacks_made=0)

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
        self.game.trigger(DeathTrigger(self.card.card_id))

    def to_json(self):
        data = {
            'hp': self.hp,
            'face_down': self.face_down,
            'attacks_made': self.attacks_made,
        }
        if self.pair:
            data['pair'] = self.pair.card.card_id
        return data
