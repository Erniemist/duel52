from Client.Actions.PlayAction import PlayAction
from Client.Card.ClientCard import ClientCard


class ClientSide:
    def __init__(self, game, lane, side_id, player):
        self.game = game
        self.lane = lane
        self.side_id = side_id
        self.player = player
        self.team = player.team
        self.cards: list[ClientCard] = []

    def can_place(self, card):
        return any(
            proposal['action'] == PlayAction.name
            and proposal['data']['card'] == card.card_id
            and proposal['data']['side'] == self.side_id
            for proposal in self.game.proposals
        )

    def on_place(self, card):
        self.game.play_action(card, self)
