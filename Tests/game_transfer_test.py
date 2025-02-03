from Client.ClientGameState import ClientGameState
from DataTransfer.GameData import GameData


def test_make_server():
    game_json = {
        'active_player_index': 0,
        'graveyard': {'cards': []},
        'players': [
            {
                'team': 'Team 1',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': [],
                'actions': 3,
            },
            {
                'team': 'Team 2',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': [],
                'actions': 0,
            },
        ],
        'board': {'lanes': [
            {'sides': [{'cards': []}, {'cards': []}]},
            {'sides': [{'cards': []}, {'cards': []}]},
            {'sides': [{'cards': []}, {'cards': []}]},
        ]},
        'winner': None,
    }
    server = GameData.from_json(game_json).make_server()
    game_data = GameData.from_server(server, 'Team 1')
    assert game_json == game_data.to_json()
    assert isinstance(game_data.make_client(), ClientGameState)
