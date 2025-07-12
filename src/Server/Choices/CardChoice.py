class CardChoice:
    def __init__(self, choice_validators, game, chooser, target=None, optional=False):
        self.game = game
        self.chooser = chooser
        self.choice_validators = choice_validators
        self.target = target
        self.optional = optional
        self.card = None
        self.resolved = False

    def submit(self, card_id, game):
        self.card = self.validate_choice(card_id, game)
        self.resolved = True

    def validate_choice(self, card_id, game):
        if card_id is None:
            if self.optional:
                return None
            raise Exception(f'No card submitted on mandatory choice')
        card = game.find_card(card_id)
        if card is None:
            raise Exception(f'Card {card_id} not found')
        for validator in self.choice_validators:
            if not validator.could_choose(card):
                raise Exception(f'{card.card_id} is not a valid {validator.name} choice')
        return card

    def could_choose(self, card):
        return all(validator.could_choose(card) for validator in self.choice_validators)
