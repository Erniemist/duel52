from Server.Triggers.Trigger import Trigger


class AttackTrigger(Trigger):
    def __init__(self, attacker_id, defender_id, player):
        self.defender_id = defender_id
        super().__init__(source_id=attacker_id, player=player)
