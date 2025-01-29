from Board.Board import Board
from Graveyard.Graveyard import Graveyard
from Player.ClientPlayer import ClientPlayer
from Server.ServerGameState import ServerGameState


class ClientGameState(ServerGameState):
    def __init__(self, active_player_index, winner, graveyard, players, board):
        self.winner = winner
        self.graveyard = Graveyard.from_json(game=self, data=graveyard)
        self.event_data = []
        self.players = [ClientPlayer.from_json(game=self, data=player_data) for player_data in players]
        self.board = Board.from_json(game=self, data=board)
        self.active_player_index=active_player_index

    def update(self):
        if len(self.event_data) > 0:
            return self.event_data.pop(0)
        return None

    def play_event(self, card, side):
        self.event('play', {'card': card.card_id, 'side': side.side_id})
        self.active_player().play_card(card=card, side=side)

    def flip_event(self, minion):
        self.event('flip', {'card': minion.card.card_id})
        self.active_player().flip_minion(minion=minion)

    def attack_event(self, minion_1, minion_2):
        self.event('attack', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})
        self.active_player().attack(friendly_minion=minion_1, enemy_minion=minion_2)

    def pair_event(self, minion_1, minion_2):
        self.event('pair', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})
        self.active_player().pair(minion=minion_1, second_minion=minion_2)

    def event(self, event, data):
        self.event_data.append({'event': event, 'data': data})

    @staticmethod
    def from_json(data):
        return ClientGameState(
            active_player_index=data['active_player_index'],
            winner=data['winner'],
            graveyard=data['graveyard'],
            players=data['players'],
            board=data['board'],
        )
