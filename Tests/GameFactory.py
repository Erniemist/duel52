from DataTransfer.GameData import GameData


class GameFactory:
    base = {
        'active_player_index': 0,
        'graveyard': {'cards': []},
        'players': [
            {
                'team': 'A',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': [],
                'actions': 2,
            },
            {
                'team': 'B',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': [],
                'actions': 0,
            },
        ],
        'board': {'lanes': [
            {'sides': [
                {'side_id': '111', 'cards': []},
                {'side_id': '222', 'cards': []},
            ]},
            {'sides': [
                {'side_id': '333', 'cards': []},
                {'side_id': '444', 'cards': []},
            ]},
            {'sides': [
                {'side_id': '555', 'cards': []},
                {'side_id': '666', 'cards': []},
            ]},
        ]},
        'winner': None,
    }

    def __init__(self):
        self.game_data = GameData.from_json(self.base)

    def with_hand(self, team, cards):
        player = next(player for player in self.game_data.players if player.team == team)
        player.hand = cards
        for card in cards:
            player.known_cards.append(card.card_id)

    def make_server(self):
        return self.game_data.make_server()
