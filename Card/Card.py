from GameState import GameState


class Card:
    def __init__(self, value: str, host, card_id, game: GameState):
        self.value = value
        self.host = host
        self.card_id = card_id
        self.player = host.player
        self.game = game

    def move_to(self, new_host):
        self.host.remove_card(self)
        self.host = new_host
        new_host.add_card(self)

    def in_graveyard(self):
        return self.card_id in [card.card_id for card in self.game.graveyard.get_cards()]

    def in_hand(self):
        return self.card_id in [card.card_id for card in self.game.get_hand_cards()]

    def on_board(self):
        return self.card_id in [card.card_id for card in self.game.board.get_cards()]
