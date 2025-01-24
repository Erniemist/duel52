from Board.Lane.Side.Minion.MinionView import MinionView


class Minion:
    max_hp = 2

    def __init__(self, card, side, game):
        self.card = card
        self.side = side
        self.game = game
        self.hp = self.max_hp
        self.face_down = True
        self.view_object = None

    def can_select(self, game):
        return game.active_player.team == self.side.team

    def on_select(self, game):
        if self.face_down:
            self.face_down = False
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
        self.damage(1)

    def view(self, position):
        damage = self.max_hp - self.hp
        self.view_object = MinionView(self, position, -90 / self.max_hp * damage)
        return self.view_object

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.die()

    def die(self):
        self.card.move_to(self.game.graveyard)
