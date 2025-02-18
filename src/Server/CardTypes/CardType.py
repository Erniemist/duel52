from functions import can_call


class CardType:
    def __init__(self, card, abilities, max_hp=2):
        self.card = card
        self.abilities = abilities
        self.max_hp = max_hp

    def handle_triggers(self, trigger):
        for ability in self.abilities:
            if can_call(ability, 'should_trigger') and ability.should_trigger(self.card, trigger):
                yield ability(self.card, self.card.game, trigger)
