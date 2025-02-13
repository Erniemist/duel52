class CardType:
    def __init__(self, card, abilities):
        self.card = card
        self.abilities = abilities

    def handle_triggers(self, trigger):
        for ability in self.abilities:
            if ability.should_trigger(self.card, trigger):
                yield ability(self.card, self.card.game, trigger)
