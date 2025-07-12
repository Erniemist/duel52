from Client.Actions.AttackAction import AttackAction
from Client.Actions.FlipAction import FlipAction
from Client.Actions.PairAction import PairAction
from Client.Board.Lane.Side.Minion.Minion import Minion
from Client.Cursor.Target import Target
from Server.CardTypes.Abilities.Stealth import Stealth


class ClientMinion(Minion):
    def __init__(self, card, game, minion_data):
        self.card = card
        self.game = game
        self.value = card.value
        self.player = self.side.player
        self.team = self.player.team
        self.max_hp = minion_data.max_hp
        self.hp = minion_data.hp
        self.face_down = minion_data.face_down
        self.attacks_made = minion_data.attacks_made
        self.max_attacks = minion_data.max_attacks
        self.frozen = minion_data.frozen
        self.pair = None
        self.view_object = None

    @property
    def side(self):
        return self.card.host

    def can_select(self):
        for proposal in self.game.proposals:
            match proposal:
                case {'action': FlipAction.name, 'data': {'card': self.card.card_id}}: return True
                case {'action': PairAction.name, 'data': {'card_1': self.card.card_id}}: return True
                case {'action': AttackAction.name, 'data': {'attacker': self.card.card_id}}: return True
                case _: continue
        return False

    def on_select(self, cursor):
        if self.face_down:
            self.game.flip_action(self)
        else:
            cursor.set_target_source(Target.harm(source=self))

    def can_hover(self, player):
        return self.card.card_id in player.known_cards

    def on_hover(self):
        pass

    def can_choose(self, valid_choices):
        return self.card in valid_choices

    def on_choose(self):
        self.game.submit_choice(self.card.card_id)

    def can_target(self):
        for proposal in self.game.proposals:
            if proposal['action'] == PairAction.name and proposal['data']['card_2'] == self.card.card_id:
                return True
            if proposal['action'] == AttackAction.name and self.card.card_id in proposal['data']['targets']:
                return True
        return False

    def on_target(self, target_source):
        if self.game.active_player().team != self.team:
            self.game.attack(target_source, self)
        else:
            self.game.pair_action(target_source, self)

    def has_active_keyword(self, keyword):
        return not self.face_down and self.card.has_keyword(keyword)
