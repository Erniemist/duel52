from copy import deepcopy

from Client.ClientGameState import ClientGameState
from DataTransfer.GameData import GameData
from GameFactory import GameFactory


def test_make_server():
    server = GameData.from_json(GameFactory.base).make_server()

    game_data = GameData.from_server(server, 'A')

    assert GameFactory.base == game_data.to_json()
    assert isinstance(game_data.make_client(), ClientGameState)


def test_graveyard():
    game_json = deepcopy(GameFactory.base)
    game_json['graveyard']['cards'] = [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
    ]
    game_json['players'][0]['known_cards'] = ['1111', '2222']

    server = GameData.from_json(game_json).make_server()

    game_data_1 = GameData.from_server(server, 'A').to_json()
    assert game_data_1['graveyard']['cards'] == [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
    ]

    game_data_2 = GameData.from_server(server, 'B').to_json()
    assert game_data_2['graveyard']['cards'] == [
        {'card_id': '1111', 'value': ''},
        {'card_id': '2222', 'value': ''},
    ]


def test_hand():
    game_json = deepcopy(GameFactory.base)
    game_json['players'][0]['hand']['cards'] = [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
    ]
    game_json['players'][0]['known_cards'] = ['1111', '2222']

    server = GameData.from_json(game_json).make_server()

    game_data_1 = GameData.from_server(server, 'A').to_json()
    assert game_data_1['players'][0]['hand']['cards'] == [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
    ]
    assert game_data_1['players'][1]['hand']['cards'] == []

    game_data_2 = GameData.from_server(server, 'B').to_json()
    assert game_data_2['players'][0]['hand']['cards'] == [
        {'card_id': '1111', 'value': ''},
        {'card_id': '2222', 'value': ''},
    ]
    assert game_data_2['players'][1]['hand']['cards'] == []


def test_deck():
    game_json = deepcopy(GameFactory.base)
    game_json['players'][0]['deck']['cards'] = [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
    ]
    game_json['players'][0]['known_cards'] = ['1111', '2222']
    server = GameData.from_json(game_json).make_server()
    game_data_1 = GameData.from_server(server, 'A').to_json()
    assert game_data_1['players'][0]['deck']['cards'] == [
        {'card_id': '1111', 'value': 'A'},
        {'card_id': '2222', 'value': '2'},
    ]
    assert game_data_1['players'][1]['deck']['cards'] == []

    game_data_2 = GameData.from_server(server, 'B').to_json()
    assert game_data_2['players'][0]['deck']['cards'] == [
        {'card_id': '1111', 'value': ''},
        {'card_id': '2222', 'value': ''},
    ]
    assert game_data_2['players'][1]['deck']['cards'] == []


def test_board():
    game_json = deepcopy(GameFactory.base)
    game_json['board']['lanes'] = [
        {'sides': [
            {'side_id': '111', 'cards': [{
                'card_id': '1111',
                'value': 'A',
                'minion': {
                    'hp': 2,
                    'face_down': True,
                    'attacks_made': 0,
                    'max_attacks': 1,
                    'frozen': False,
                },
            }]},
            {'side_id': '222', 'cards': []},
        ]},
        {'sides': [{'side_id': '333', 'cards': []}, {'side_id': '444', 'cards': []}]},
        {'sides': [{'side_id': '555', 'cards': []}, {'side_id': '666', 'cards': []}]},
    ]
    game_json['players'][0]['known_cards'] = ['1111']

    server = GameData.from_json(game_json).make_server()
    game_data_1 = GameData.from_server(server, 'A').to_json()

    assert game_data_1['board']['lanes'] == [
        {'sides': [
            {'side_id': '111', 'cards': [{
                'card_id': '1111',
                'value': 'A',
                'minion': {
                    'hp': 2,
                    'face_down': True,
                    'attacks_made': 0,
                    'max_attacks': 1,
                    'frozen': False,
                },
            }]},
            {'side_id': '222', 'cards': []},
        ]},
        {'sides': [{'side_id': '333', 'cards': []}, {'side_id': '444', 'cards': []}]},
        {'sides': [{'side_id': '555', 'cards': []}, {'side_id': '666', 'cards': []}]},
    ]

    game_data_2 = GameData.from_server(server, 'B').to_json()
    assert game_data_2['board']['lanes'] == [
        {'sides': [
            {'side_id': '111', 'cards': [{
                'card_id': '1111',
                'value': '',
                'minion': {
                    'hp': 2,
                    'face_down': True,
                    'attacks_made': 0,
                    'max_attacks': 1,
                    'frozen': False,
                },
            }]},
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
    ]
