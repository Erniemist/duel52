from Client.Action import Action
from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_play_card():
    factory = GameFactory()
    factory.with_hand('Team 1', [CardData('1234', '6')])
    server_app = ServerApp('test', factory.make_server())
    server_app.resolve_action(Action.play('1234', '222').json())
    client_game = GameData.from_server(server_app.game, 'Team 1').make_client()

    assert len(client_game.players[0].hand.cards) == 0
    played_card = client_game.board.lanes[0].sides[1].cards[0]
    assert played_card.card_id == '1234'
    assert played_card.value == '6'
