from Client.Card.ClientCard import ClientCard


class ClientGraveyard:
    def __init__(self, game, graveyard_data):
        self.game = game
        self.cards: dict[str, ClientCard] = graveyard_data.build(game, self)
