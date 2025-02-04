from Client.Action import Action
from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_three():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'A'),
        CardData('2222', '2'),
        CardData('3333', '3'),
    ])
    factory.with_hand('B', [
        CardData('4444', '4'),
        CardData('5555', '5'),
    ])
    server_app = ServerApp('test', factory.make_server())

    server_app.resolve_action(Action.play('1111', '111').json())
    server_app.resolve_action(Action.play('3333', '111').json())

    server_app.resolve_action(Action.play('4444', '222').json())
    server_app.resolve_action(Action.flip('4444').json())
    server_app.resolve_action(Action.attack('4444', '3333').json())

    server_app.resolve_action(Action.flip('1111').json())
    server_app.resolve_action(Action.play('2222', '111').json())
    server_app.resolve_action(Action.flip('2222').json())

    server_app.resolve_action(Action.attack('4444', '3333').json())

    client_game = GameData.from_server(server_app.game, 'A').make_client()

    assert client_game.find_card_from_board('3333') is not None
    assert not client_game.find_card_from_board('3333').minion.face_down
    assert '3333' not in client_game.graveyard.cards.keys()
