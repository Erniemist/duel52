import pytest

from Client.Action import Action
from DataTransfer.CardData import CardData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_six_freezes():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('6666', '6'),
    ])
    factory.with_hand('B', [
        CardData('3333', 'X'),
        CardData('4444', 'X'),
        CardData('5555', 'X'),
    ])
    server_app = ServerApp('test', factory.make_server())

    server_app.resolve_action(Action.play('6666', '111').json())

    server_app.game.new_turn()
    server_app.resolve_action(Action.play('3333', '222').json())
    server_app.resolve_action(Action.play('4444', '222').json())
    server_app.resolve_action(Action.flip('4444').json())

    server_app.resolve_action(Action.flip('6666').json())

    server_app.game.new_turn()
    server_app.resolve_action(Action.play('5555', '222').json())
    server_app.resolve_action(Action.flip('5555').json())

    with pytest.raises(Exception, match='Frozen minion 3333 cannot flip'):
        server_app.resolve_action(Action.flip('3333').json())
    with pytest.raises(Exception, match='Frozen minion 4444 cannot attack'):
        server_app.resolve_action(Action.attack('4444', '6666').json())
    with pytest.raises(Exception, match='Frozen minion 4444 cannot pair'):
        server_app.resolve_action(Action.pair('4444', '5555').json())
    with pytest.raises(Exception, match='Frozen minion 4444 cannot pair'):
        server_app.resolve_action(Action.pair('5555', '4444').json())


def test_six_wears_off():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('6666', '6'),
    ])
    factory.with_hand('B', [
        CardData('3333', 'X'),
        CardData('4444', 'X'),
        CardData('5555', 'X'),
    ])
    server_app = ServerApp('test', factory.make_server())

    server_app.resolve_action(Action.play('6666', '111').json())

    server_app.game.new_turn()
    server_app.resolve_action(Action.play('3333', '222').json())

    server_app.game.new_turn()
    server_app.resolve_action(Action.flip('6666').json())

    server_app.game.new_turn()
    server_app.game.new_turn()
    server_app.game.new_turn()
    server_app.resolve_action(Action.flip('3333').json())
    assert not server_app.game.find_card_from_board('3333').minion.face_down
