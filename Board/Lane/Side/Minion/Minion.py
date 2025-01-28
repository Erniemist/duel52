import json


class Minion:
    max_hp = 2
    max_attacks = 1

    def __init__(self, card, side, game):
        self.card = card
        self.value = card.value
        self.side = side
        self.player = side.player
        self.team = self.player.team
        self.game = game
        self.hp = self.max_hp
        self.face_down = True
        self.view_object = None
        self.pair = None
        self.attacks_made = 0

    def end_turn(self):
        self.attacks_made = 0

    def attacks_left(self):
        return self.max_attacks - (self.attacks_made + (self.pair.attacks_made if self.pair else 0))

    def can_select(self, game):
        if self.team != game.active_player().team or self.player.actions < 1:
            return False
        return not self.pair or self.attacks_left() > 0

    def on_select(self, game):
        if self.face_down:
            game.active_player().flip_card(self)
        else:
            game.cursor.set_target_source(self)

    def can_target(self, game, target_source):
        if game.active_player().team != self.team:
            return self.can_be_attacked(target_source)
        return self.can_pair(target_source)

    def can_be_attacked(self, target_source):
        if target_source.attacks_left() < 1:
            return False
        return target_source.side.lane == self.side.lane

    def can_pair(self, target_source):
        if self.face_down:
            return False
        if self.pair or target_source.pair:
            return False
        return self.value == target_source.value

    def on_target(self, game, target_source):
        game.cursor.cancel_target()
        if game.active_player().team != self.team:
            game.active_player().attack(target_source, self)
        else:
            game.active_player().pair_cards(target_source, self)

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

    def to_json(self):
        data = {
            'hp': self.hp,
            'face_down': self.face_down,
            'attacks_made': self.attacks_made,
        }
        if self.pair:
            data['pair'] = self.pair.card.card_id
        return data

    @staticmethod
    def from_json(card, side, game, data):
        minion = Minion(card=card, side=side, game=game)
        minion.hp = data['hp']
        minion.face_down = data['face_down']
        minion.attacks_made = data['attacks_made']
        return minion
