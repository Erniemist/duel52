from DataTransfer.GameData import GameData
from Server.ServerApp import ServerApp


def test_play_card():
    game_json = {
        'active_player_index': 0,
        'graveyard': {'cards': []},
        'players': [
            {
                'team': 'Team 1',
                'hand': {'cards': [{
                    'card_id': '1234',
                    'value': 'A',
                }]},
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
    server_app = ServerApp('test', GameData.from_json(game_json).make_server())
    server_app.resolve_action({'action': 'play', 'data': {'side': '222', 'card': '1234'}})

    assert len(server_app.game.players[0].hand.cards) == 0
    played_card = server_app.game.board.lanes[0].sides[1].cards[0]
    assert played_card.card_id == '1234'
    assert played_card.value == 'A'
