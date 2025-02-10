class Hand:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        self.player.learn(card)

    def remove_card(self, card):
        self.cards = [c for c in self.cards if c is not card]

    def contains(self, card):
        for my_card in self.cards:
            if my_card.card_id == card.card_id:
                return True
        return False
