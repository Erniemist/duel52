from Client.Board.ClientBoard import ClientBoard
from Client.Card.ClientCard import ClientCard
from Client.Event import Event
from Client.Graveyard.ClientGraveyard import ClientGraveyard
from Client.Player.ClientPlayer import ClientPlayer


class ClientGameState:
    def __init__(self, game_data):
        graveyard, players, board = game_data.build_for_client(self)
        self.winner = game_data.winner
        self.graveyard: ClientGraveyard = graveyard
        self.players: list[ClientPlayer] = players
        self._active_player: ClientPlayer = self.players[game_data.active_player_index]
        self.board: ClientBoard = board
        self.events = []

    def active_player(self):
        return self._active_player

    def find_card_from_board(self, card_id) -> None | ClientCard:
        return next((card for card in self.board.get_cards() if card.card_id == card_id))

    def find_card_from_hand(self, card_id) -> None | ClientCard:
        for player in self.players:
            for card in player.hand.cards:
                if card.card_id == card_id:
                    return card
        return None

    def play_event(self, card, side):
        self.event('play', {'card': card.card_id, 'side': side.side_id})

    def flip_event(self, minion):
        self.event('flip', {'card': minion.card.card_id})

    def attack_event(self, minion_1, minion_2):
        self.event('attack', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})

    def pair_event(self, minion_1, minion_2):
        self.event('pair', {'card_1': minion_1.card.card_id, 'card_2': minion_2.card.card_id})

    def event(self, name, data):
        self.events.append(Event(event_id=len(self.events), name=name, data=data))

    def next_event(self):
        return next((event for event in self.events if not event.resolved), None)

    def resolve(self, event_id):
        self.events[event_id].resolved = True
