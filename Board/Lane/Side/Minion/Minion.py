from Board.Lane.Side.Minion.MinionView import MinionView


class Minion:
    max_hp = 2
    max_attacks = 1

    def __init__(self, card, side, game):
        self.card = card
        self.side = side
        self.player = side.player
        self.team = self.player.team
        self.game = game
        self.hp = self.max_hp
        self.face_down = True
        self.view_object = None
        self.pair = None
        self.attacks_left = self.max_attacks

    def start_turn(self):
        self.attacks_left = self.max_attacks

    def can_select(self, game):
        return self.team == game.active_player().team and self.player.actions > 0 and self.attacks_left > 0

    def on_select(self, game):
        if self.face_down:
            game.active_player().flip_card(self)
        else:
            game.cursor.set_target_source(self)

    def can_target(self, game, target_source):
        if target_source.side.lane is not self.side.lane:
            return False
        if target_source.side.team == self.side.team:
            return False
        return True

    def on_target(self, game, target_source):
        game.cursor.cancel_target()
        if target_source.side.lane is not self.side.lane:
            return
        if target_source.side is self.side:
            return
        game.active_player().attack(target_source, self)

    def view(self, position):
        damage = self.max_hp - self.hp
        self.view_object = MinionView(self, position, -90 / self.max_hp * damage)
        return self.view_object

    def attack(self, enemy):
        self.attacks_left -= 1
        damage = 2 if self.pair else 1
        enemy.hp -= damage
        if enemy.hp <= 0:
            enemy.die()

    def die(self):
        self.card.move_to(self.game.graveyard)
