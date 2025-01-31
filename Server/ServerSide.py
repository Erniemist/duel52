from Board.Lane.Side.Side import Side


class ServerSide(Side):
    def __init__(self, game, lane, side_id, player):
        super().__init__(game, lane, side_id, player)

    def to_json(self, player):
        return {'cards': [card.to_json(player) for card in self.cards]}
