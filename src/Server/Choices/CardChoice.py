class CardChoice:
    def __init__(self, choice_validators, game):
        self.game = game
        self.choice_validators = choice_validators
        self.card = None
        self.resolved = False

    def submit(self, card_id, game):
        self.card = game.find_card(card_id)
        if self.card is None:
            raise Exception(f'Card {card_id} not found')
        for validator in self.choice_validators:
            if not validator.could_choose(self.card):
                raise Exception(f'{self.card.card_id} is not a valid {validator.name} choice')
        self.resolved = True

    def could_choose(self, card):
        return all(validator.could_choose(card) for validator in self.choice_validators)
