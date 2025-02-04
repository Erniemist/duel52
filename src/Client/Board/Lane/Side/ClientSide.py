from Client.Card.ClientCard import ClientCard


class ClientSide:
    def __init__(self, game, lane, side_id, player):
        self.game = game
        self.lane = lane
        self.side_id = side_id
        self.player = player
        self.team = player.team
        self.cards: list[ClientCard] = []

    def can_place(self, card, my_turn):
        return my_turn and self.team == self.game.active_player().team and self.player.actions > 0

    def on_place(self, card):
        self.game.play_action(card, self)
