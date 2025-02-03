from Client.Card.ClientCard import ClientCard


class ClientSide:
    def __init__(self, game, lane, side_id, player, cards_data):
        self.game = game
        self.lane = lane
        self.side_id = side_id
        self.player = player
        self.team = player.team
        self.cards: list[ClientCard] = []
        for card_data in cards_data:
            self.cards.append(ClientCard.from_json(host=self, game=game, data=card_data))

    def can_place(self, card, my_turn):
        return my_turn and self.team == self.game.active_player().team and self.player.actions > 0

    def on_place(self, card):
        self.game.play_event(card, self)

    @staticmethod
    def from_json(lane, player, side_id, game, data):
        return ClientSide(game=game, lane=lane, side_id=side_id, player=player, cards_data=data['cards'])
