from Client.Actions.Action import Action


class AttackAction(Action):
    name = 'attack'

    def __init__(self, attacker, targets):
        self.attacker = attacker
        self.targets = targets
        super().__init__()

    def data(self):
        return {'attacker': self.attacker, 'targets': self.targets}
