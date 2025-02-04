from Client.Action import Action
from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_five():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('5555', '5'),
    ])
    server_app = ServerApp('test', factory.make_server())

    server_app.resolve_action(Action.play('5555', '111').json())
    server_app.resolve_action(Action.play('1111', '111').json())
    server_app.resolve_action(Action.play('2222', '111').json())
    server_app.resolve_action(Action.flip('5555').json())

    side = server_app.game.board.lanes[0].sides[0]
    assert not side.cards[0].minion.face_down
    assert not side.cards[1].minion.face_down
    assert not side.cards[2].minion.face_down
