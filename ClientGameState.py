from Board.Board import Board
from GameState import GameState
from Graveyard.Graveyard import Graveyard
from Player.Player import Player


class ClientGameState(GameState):
    def __init__(self):
        self.event_data = []
        super().__init__()

    def update(self):
        if len(self.event_data) > 0:
            return self.event_data.pop(0)
        return None

    def play_event(self, card, side):
        self.event('play', {'card': card.card_id, 'side': side.side_id})

    def flip_event(self, minion):
        self.event('flip', {'card': minion.card.card_id})

    def attack_event(self, minion_1, minion_2):
        self.event('attack', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})

    def pair_event(self, minion_1, minion_2):
        self.event('pair', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})

    def event(self, event, data):
        self.event_data.append({'event': event, 'data': data})

    @staticmethod
    def from_json(data):
        game = ClientGameState()
        game.active_player_index = data['active_player_index']
        game.winner = data['winner']
        game.graveyard = Graveyard.from_json(game=game, data=data['graveyard'])
        game.players = [Player.from_json(game=game, data=player_data) for player_data in data['players']]
        game.board = Board.from_json(game=game, data=data['board'])
        return game
