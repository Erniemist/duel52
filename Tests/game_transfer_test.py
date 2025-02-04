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
        'graveyard': {'cards': [
            {'card_id': '1111', 'value': 'A'},
            {'card_id': '2222', 'value': '2'},
            {'card_id': '3333', 'value': '3'},
            {'card_id': '4444', 'value': '4'},
        ]},
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
    server = GameData.from_json(game_json).make_server()
    game_data_1 = GameData.from_server(server, 'Team 1').to_json()
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


def test_hand():
    game_json = {
        'active_player_index': 0,
        'graveyard': {'cards': []},
        'players': [
            {
                'team': 'Team 1',
                'hand': {'cards': [
                    {'card_id': '1111', 'value': 'A'},
                    {'card_id': '2222', 'value': '2'},
                    {'card_id': '3333', 'value': '3'},
                    {'card_id': '4444', 'value': '4'},
                ]},
                'deck': {'cards': []},
                'known_cards': ['1111', '2222', '3333', '4444'],
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
    game_data_1 = GameData.from_server(server, 'Team 1').to_json()
    assert game_data_1['players'][0]['hand']['cards'] == [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
        {'card_id': '3333', 'value': '3'},
        {'card_id': '4444', 'value': '4'},
    ]
    assert game_data_1['players'][1]['hand']['cards'] == []

    game_data_2 = GameData.from_server(server, 'Team 2').to_json()
    assert game_data_2['players'][0]['hand']['cards'] == [
        {'card_id': '1111', 'value': ''},
        {'card_id': '2222', 'value': ''},
        {'card_id': '3333', 'value': ''},
        {'card_id': '4444', 'value': ''},
    ]
    assert game_data_2['players'][1]['hand']['cards'] == []


def test_deck():
    game_json = {
        'active_player_index': 0,
        'graveyard': {'cards': []},
        'players': [
            {
                'team': 'Team 1',
                'hand': {'cards': []},
                'deck': {'cards': [
                    {'card_id': '1111', 'value': 'A'},
                    {'card_id': '2222', 'value': '2'},
                    {'card_id': '3333', 'value': '3'},
                    {'card_id': '4444', 'value': '4'},
                ]},
                'known_cards': ['1111', '2222', '3333', '4444'],
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
    game_data_1 = GameData.from_server(server, 'Team 1').to_json()
    assert game_data_1['players'][0]['deck']['cards'] == [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
        {'card_id': '3333', 'value': '3'},
        {'card_id': '4444', 'value': '4'},
    ]
    assert game_data_1['players'][1]['deck']['cards'] == []

    game_data_2 = GameData.from_server(server, 'Team 2').to_json()
    assert game_data_2['players'][0]['deck']['cards'] == [
        {'card_id': '1111', 'value': ''},
        {'card_id': '2222', 'value': ''},
        {'card_id': '3333', 'value': ''},
        {'card_id': '4444', 'value': ''},
    ]
    assert game_data_2['players'][1]['deck']['cards'] == []

def test_board():
    game_json = {
        'active_player_index': 0,
        'graveyard': {'cards': []},
        'players': [
            {
                'team': 'Team 1',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': ['1111', '3333', '5555'],
                'actions': 3,
            },
            {
                'team': 'Team 2',
                'hand': {'cards': []},
                'deck': {'cards': []},
                'known_cards': ['2222', '4444', '6666'],
                'actions': 0,
            },
        ],
        'board': {'lanes': [
            {'sides': [
                {'cards': [{'card_id': '1111', 'value': 'A'}]},
                {'cards': [{'card_id': '2222', 'value': '2'}]},
            ]},
            {'sides': [
                {'cards': [{'card_id': '3333', 'value': '3'}]},
                {'cards': [{'card_id': '4444', 'value': '4'}]},
            ]},
            {'sides': [
                {'cards': [{'card_id': '5555', 'value': '5'}]},
                {'cards': [{'card_id': '6666', 'value': '6'}]},
            ]},
        ]},
        'winner': None,
    }
    server = GameData.from_json(game_json).make_server()
    game_data_1 = GameData.from_server(server, 'Team 1').to_json()
    assert game_data_1['board']['lanes'] == [
        {'sides': [
            {'cards': [{'card_id': '1111', 'value': 'A'}]},
            {'cards': [{'card_id': '2222', 'value': ''}]},
        ]},
        {'sides': [
            {'cards': [{'card_id': '3333', 'value': '3'}]},
            {'cards': [{'card_id': '4444', 'value': ''}]},
        ]},
        {'sides': [
            {'cards': [{'card_id': '5555', 'value': '5'}]},
            {'cards': [{'card_id': '6666', 'value': ''}]},
        ]},
    ]

    game_data_2 = GameData.from_server(server, 'Team 2').to_json()
    assert game_data_2['board']['lanes'] == [
        {'sides': [
            {'cards': [{'card_id': '1111', 'value': ''}]},
            {'cards': [{'card_id': '2222', 'value': '2'}]},
        ]},
        {'sides': [
            {'cards': [{'card_id': '3333', 'value': ''}]},
            {'cards': [{'card_id': '4444', 'value': '4'}]},
        ]},
        {'sides': [
            {'cards': [{'card_id': '5555', 'value': ''}]},
            {'cards': [{'card_id': '6666', 'value': '6'}]},
        ]},
    ]
