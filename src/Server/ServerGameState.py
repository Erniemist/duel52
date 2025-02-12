import random
import uuid

from Server.Actions.AttackAction import AttackAction
from Server.Actions.FlipAction import FlipAction
from Server.Actions.PairAction import PairAction
from Server.Actions.PlayAction import PlayAction
from DataTransfer.CardData import CardData
from Server.Effects.Effect import Effect
from Server.ServerBoard import ServerBoard
from Server.ServerCard import ServerCard
from Client.Deck.Deck import Deck
from Server.ServerGraveyard import ServerGraveyard
from Server.ServerPlayer import ServerPlayer


class ServerGameState:
    def __init__(self, game_data=None):
        self.triggers = []
        self.awaited_choices = []
        self.abilities = []
        if game_data is None:
            self.winner: None | ServerPlayer = None
            self.active_player_index = random.randint(0, 1)
            self.graveyard: ServerGraveyard = ServerGraveyard(self)
            self.players: list[ServerPlayer] = self.make_players(self.make_deck())
            self.board: ServerBoard = ServerBoard(self, self.players)
            self.active_player().start_turn(actions=2)
        else:
            graveyard, players, board = game_data.build(self)
            self.winner = game_data.winner
            self.active_player_index = game_data.active_player_index
            self.graveyard: ServerGraveyard = graveyard
            self.players: list[ServerPlayer] = players
            self.board: ServerBoard = board

    def active_player(self) -> ServerPlayer:
        return self.players[self.active_player_index]

    def player_by_team(self, team):
        return next(player for player in self.players if player.team == team)

    def make_players(self, main_deck: Deck) -> list[ServerPlayer]:
        players = []
        for team in ['A', 'B']:
            player = ServerPlayer(team, self)
            for i in range(20):
                main_deck.draw_from_top(player.deck)
            for i in range(5):
                player.deck.draw_from_top(player.hand)
            players.append(player)
        return players

    def make_deck(self) -> Deck:
        main_deck = Deck(self, None)
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        cards = [
            CardData(str(uuid.uuid4().int), value).make(self, main_deck, True)
            for card_id, value in enumerate(values)
        ]
        random.shuffle(cards)
        main_deck.cards = cards
        return main_deck

    def check_victory(self):
        self.winner = self.determine_winner()

    def determine_winner(self) -> None | ServerPlayer:
        if not self.all_cards_played():
            return None
        lanes_won = {player.team: 0 for player in self.players}
        for lane in self.board.lanes:
            winner = lane.player_winning_lane()
            if winner is not None:
                lanes_won[winner.team] += 1
        for player in self.players:
            if lanes_won[player.team] > 1:
                return player
        return None

    def all_cards_played(self):
        return all(len(player.deck.cards) + len(player.hand.cards) == 0 for player in self.players)

    def find_side(self, side_id):
        for lane in self.board.lanes:
            for side in lane.sides:
                if side.side_id == side_id:
                    return side
        return None

    def find_card_from_board(self, card_id) -> ServerCard:
        return next((card for card in self.board.get_cards() if card.card_id == card_id))

    def find_card_from_hand(self, card_id) -> None | ServerCard:
        return next((card for card in self.get_hand_cards() if card.card_id == card_id), None)

    def find_card(self, card_id):
        return self.find_card_from_hand(card_id) or self.find_card_from_board(card_id)

    def get_hand_cards(self):
        return (card for player in self.players for card in player.hand.cards)

    def get_cards(self):
        return [
            *self.board.get_cards(),
            *self.graveyard.cards.values(),
            *self.get_hand_cards(),
        ]

    def play(self, card_id, side_id):
        self.resolve_action(PlayAction(self, card_id, side_id))

    def flip(self, card_id):
        self.resolve_action(FlipAction(self, card_id))

    def pair(self, card_1_id, card_2_id):
        self.resolve_action(PairAction(self, card_1_id, card_2_id))

    def attack(self, card_1_id, card_2_id):
        self.resolve_action(AttackAction(self, card_1_id, card_2_id))

    def resolve_action(self, action):
        self.active_player().start_action()
        action.resolve()
        self.active_player().finish_action()
        self.resolve_triggers()
        self.resolve_abilities()
        self.resolve_triggers()

    def awaiting_choice(self):
        return len(self.awaited_choices) > 0

    def choose(self, card_id):
        requirement = self.awaited_choices.pop(0)
        requirement.submit(card_id, self)
        self.resolve_abilities()
        self.resolve_triggers()

    def trigger(self, trigger):
        self.triggers.append(trigger)

    def resolve_triggers(self):
        while len(self.triggers) > 0:
            trigger = self.triggers.pop()
            for card in self.get_cards():
                if card.type:
                    abilities = card.type.handle_triggers(trigger)
                    if abilities is not None:
                        self.abilities += [*abilities]

    def resolve_abilities(self):
        while len(self.abilities) > 0:
            ability = self.abilities[0]
            for next_step in ability.unresolved_parts():
                if isinstance(next_step, Effect):
                    next_step.resolve()
                else:
                    self.awaited_choices.append(next_step)
                    return
            self.abilities.pop(0)

    def new_turn(self):
        self.active_player().end_turn()
        self.active_player_index = (self.active_player_index + 1) % 2
        self.active_player().start_turn()
