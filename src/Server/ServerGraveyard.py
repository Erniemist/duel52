from Server.ServerCard import ServerCard


class ServerGraveyard:
    def __init__(self, game, graveyard_data=None):
        self.game = game
        if graveyard_data is None:
            self.cards = {}
        else:
            self.cards: dict[str, ServerCard] = graveyard_data.build_for_server(game, self)

    def add_card(self, card):
        self.cards[card.card_id] = card

    def remove_card(self, card):
        self.cards.pop(card.card_id)

