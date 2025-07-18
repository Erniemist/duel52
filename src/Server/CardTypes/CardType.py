from functions import can_call


class CardType:
    def __init__(self, card, name='', max_hp=2, abilities=None):
        self.card = card
        self.name = name
        self.max_hp = max_hp
        self.abilities = abilities if abilities else []

    def handle_triggers(self, trigger):
        for ability in self.abilities:
            if can_call(ability, 'should_trigger') and ability.should_trigger(self.card, trigger):
                yield ability(self.card, self.card.game, trigger)
