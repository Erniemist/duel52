from DataTransfer.CardData import CardData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_choosing():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('X_1', 'X'),
    ])
    factory.with_hand('B', [
        CardData('4', '4'),
    ])
    game = factory.make_server()
    server = ServerApp('name', game)
    game.active_player().actions = 1

    game.play('X_1', '111')

    game.active_player().actions = 2
    game.play('4', '222')
    server.resolve_action({'action': 'flip', 'data': {'card': '4'}}, 'B')
    assert game.active_player().team == 'B'
    assert game.awaiting_choice()
    assert game.awaited_choices[0].chooser.team == 'B'
    assert len(game.player_by_team('B').known_cards) == 1

    server.resolve_action({'action': 'choose', 'data': {'card': 'X_1'}}, 'B')
    assert not game.awaiting_choice()
    assert len(game.player_by_team('B').known_cards) == 2


def test_choosing_with_no_legal_target():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('X_1', 'X'),
    ])
    factory.with_hand('B', [
        CardData('4', '4'),
    ])
    game = factory.make_server()
    server = ServerApp('name', game)

    game.play('X_1', '111')
    game.flip('X_1')

    game.play('4', '222')
    server.resolve_action({'action': 'flip', 'data': {'card': '4'}}, 'B')
    assert not game.awaiting_choice()

