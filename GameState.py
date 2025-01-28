import json
import random

from Board.Board import Board
from Card.Card import Card
from Deck.Deck import Deck
from Graveyard.Graveyard import Graveyard
from Player.Player import Player


class GameState:
    def __init__(self):
        self.event_data = []
        self.graveyard = None
        self.players = []
        self.board = None
        self.active_player_index = 0
        self.turns = 0
        self.winner = None

    def start_game(self):
        self.graveyard = Graveyard(self)
        deck = self.make_deck()
        self.players = self.make_players(deck)
        self.board = Board(self)
        for player in self.players:
            player.start_game()
        self.active_player().start_turn(actions=2)

    def make_players(self, main_deck):
        players = []
        for team in Player.TEAMS:
            deck = Deck(self)
            for i in range(20):
                main_deck.draw_from_top(deck)
            players.append(Player(team, self, deck))
        return players

    def make_deck(self):
        main_deck = Deck(self)
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        cards = [
            Card(value=value, host=main_deck, card_id=card_id, game=self)
            for card_id, value in enumerate(values)
        ]
        random.shuffle(cards)
        main_deck.cards = cards
        return main_deck

    def update(self):
        if len(self.event_data) > 0:
            return self.event_data.pop(0)
        return None

    def check_victory(self):
        self.winner = self.determine_winner()

    def determine_winner(self):
        if not self.all_cards_played():
            return None
        lanes_won = {player.team: 0 for player in self.players}
        for lane in self.board.lanes:
            winner = lane.player_winning_lane()
            if winner is not None:
                lanes_won[winner] += 1
        for player in self.players:
            if lanes_won[player.team] > 1:
                return player.team
        return None

    def all_cards_played(self):
        return all(len(player.deck.cards) + len(player.hand.cards) == 0 for player in self.players)

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

    def active_player(self):
        return self.players[self.active_player_index]

    def find_card_from_hand(self, card_id):
        for player in self.players:
            for card in player.hand.cards:
                if card.card_id == card_id:
                    return card
        return None

    def find_card_from_board(self, card_id):
        for lane in self.board.lanes:
            for side in lane.sides:
                card = side.find_card(card_id)
                if card:
                    return card
        return None

    def find_side(self, side_id):
        for lane in self.board.lanes:
            for side in lane.sides:
                if side.side_id == side_id:
                    return side
        return None

    def new_turn(self):
        self.turns += 1
        self.active_player().end_turn()
        self.active_player_index = (self.active_player_index + 1) % 2
        self.active_player().start_turn()

    def to_json(self):
        return {
            'active_player_index': self.active_player_index,
            'graveyard': self.graveyard.to_json(),
            'players': [player.to_json() for player in self.players],
            'board': self.board.to_json(),
            'turns': self.turns,
            'winner': self.winner,
        }

    @staticmethod
    def from_json(data):
        game = GameState()
        game.active_player_index = data['active_player_index']
        game.turns = data['turns']
        game.winner = data['winner']
        game.graveyard = Graveyard.from_json(game=game, data=data['graveyard'])
        game.players = [Player.from_json(game=game, data=player_data) for player_data in data['players']]
        game.board = Board.from_json(game=game, data=data['board'])
        return game
