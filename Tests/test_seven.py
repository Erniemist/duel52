import pytest

from Client.Action import Action
from DataTransfer.CardData import CardData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_seven():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('7777', '7'),
    ])
    factory.with_hand('B', [
        CardData('3333', 'X'),
        CardData('4444', 'X'),
        CardData('5555', 'X'),
    ])
    server_app = ServerApp('test', factory.make_server())

    server_app.resolve_action(Action.play('1111', '111').json())
    server_app.resolve_action(Action.play('7777', '111').json())

    server_app.resolve_action(Action.play('4444', '222').json())
    server_app.resolve_action(Action.flip('4444').json())
    server_app.resolve_action(Action.attack('4444', '1111').json())

    server_app.resolve_action(Action.flip('1111').json())
    server_app.resolve_action(Action.attack('1111', '4444').json())
    server_app.resolve_action(Action.play('2222', '111').json())

    server_app.resolve_action(Action.flip('7777').json())

    assert server_app.game.find_card_from_board('1111').minion.hp == 2
    assert server_app.game.find_card_from_board('2222').minion.hp == 2
    assert server_app.game.find_card_from_board('7777').minion.hp == 2

    assert server_app.game.find_card_from_board('4444').minion.hp == 1
