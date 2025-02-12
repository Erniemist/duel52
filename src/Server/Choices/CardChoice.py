class CardChoice:
    def __init__(self, choice_type, game):
        self.game = game
        self.choice_type = choice_type
        self.card = None
        self.resolved = False

    def submit(self, card_id, game):
        self.card = game.find_card(card_id)
        if self.card is None:
            raise Exception(f'Card {card_id} not found')
        if not self.choice_type.could_choose(self.card):
            raise Exception(f'{self.card.card_id} is not a valid {self.choice_type.name} choice')
        self.resolved = True

    def could_choose(self, card):
        return self.choice_type.could_choose(card)
