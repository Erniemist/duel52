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


def test_graveyard():
    game_json = {
        'active_player_index': 0,
        'graveyard': {'cards': []},
        'players': [
            {
                'team': 'Team 1',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': ['1111', '2222'],
                'actions': 3,
            },
            {
                'team': 'Team 2',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': ['1111', '3333'],
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
    cards = {
        '1111': 'A',
        '2222': '2',
        '3333': '3',
        '4444': '4',
    }
    for card_id, value in cards.items():
        game_json['graveyard']['cards'].append({
            'card_id': card_id,
            'value': value,
        })
    server = GameData.from_json(game_json).make_server()
    game_data_1 = GameData.from_server(server, 'Team 1').to_json()
    print(game_data_1)
    assert game_data_1['graveyard']['cards'] == [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
        {'card_id': '3333', 'value': ''},
        {'card_id': '4444', 'value': ''},
    ]
    game_data_2 = GameData.from_server(server, 'Team 2').to_json()
    assert game_data_2['graveyard']['cards'] == [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': ''},
        {'card_id': '3333', 'value': '3'},
        {'card_id': '4444', 'value': ''},
    ]
