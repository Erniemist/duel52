from Board.Lane.Side.Side import Side


class Lane:
    def __init__(self, game):
        self.game = game
        self.sides = [Side(game, self, player.team) for player in game.players]
