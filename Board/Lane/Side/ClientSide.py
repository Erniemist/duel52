from Board.Lane.Side.Side import Side
from Card.ClientCard import ClientCard


class ClientSide(Side):
    def __init__(self, game, lane, side_id, player, cards_data):
        super().__init__(game, lane, side_id, player)
        for card_data in cards_data:
            self.cards.append(ClientCard.from_json(host=self, game=game, data=card_data))

    def can_place(self, card, my_turn):
        return my_turn and self.team == self.game.active_player().team and self.player.actions > 0

    def on_place(self, card):
        self.game.play_event(card, self)

    @staticmethod
    def from_json(lane, player, side_id, game, data):
        return ClientSide(game=game, lane=lane, side_id=side_id, player=player, cards_data=data['cards'])
