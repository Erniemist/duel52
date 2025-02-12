from DataTransfer.CardData import CardData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_choosing():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
    ])
    factory.with_hand('B', [
        CardData('4444', '4'),
    ])
    game = factory.make_server()
    server = ServerApp('name', game)
    game.active_player().actions = 1

    game.play('1111', '111')

    game.active_player().actions = 2
    game.play('4444', '222')
    server.resolve_action({'action': 'flip', 'data': {'card': '4444'}}, 'B')
    assert game.active_player().team == 'B'
    assert game.awaiting_choice()
    assert game.awaited_choices[0].chooser.team == 'B'
    assert len(game.player_by_team('B').known_cards) == 1

    server.resolve_action({'action': 'choose', 'data': {'card': '1111'}}, 'B')
    assert not game.awaiting_choice()
    assert len(game.player_by_team('B').known_cards) == 2
