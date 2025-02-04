from Client.Action import Action
from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory
from Server.ServerApp import ServerApp


def test_play_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('1234', '6')])
    server_app = ServerApp('test', factory.make_server())
    server_app.resolve_action(Action.play('1234', '111').json())
    client_game_1 = GameData.from_server(server_app.game, 'A').make_client()

    assert len(client_game_1.players[0].hand.cards) == 0
    played_card = client_game_1.board.lanes[0].sides[0].cards[0]
    assert played_card.card_id == '1234'
    assert played_card.value == '6'
    assert played_card.minion is not None
    assert played_card.minion.team == 'A'
    assert played_card.minion.hp == 2
    assert played_card.minion.attacks_made == 0

    client_game_2 = GameData.from_server(server_app.game, 'B').make_client()
    played_card = client_game_2.board.lanes[0].sides[0].cards[0]
    assert played_card.card_id == '1234'
    assert played_card.value == ''
    assert played_card.minion is not None
    assert played_card.minion.team == 'A'
    assert played_card.minion.hp == 2
    assert played_card.minion.attacks_made == 0


def test_flip_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('1111', 'A'), CardData('2222', '2')])
    factory.with_hand('B', [CardData('3333', '3'), CardData('4444', '4')])
    server_app = ServerApp('test', factory.make_server())
    server_app.resolve_action(Action.play('1111', '111').json())
    server_app.resolve_action(Action.flip('1111').json())
    client_game_1 = GameData.from_server(server_app.game, 'A').make_client()

    card = client_game_1.board.lanes[0].sides[0].cards[0]
    assert card.card_id == '1111'
    assert card.value == 'A'

    client_game_2 = GameData.from_server(server_app.game, 'B').make_client()
    card = client_game_2.board.lanes[0].sides[0].cards[0]
    assert card.card_id == '1111'
    assert card.value == 'A'


def test_attack_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('1111', 'A'), CardData('2222', '2')])
    factory.with_hand('B', [CardData('3333', '3'), CardData('4444', '4')])
    server_app = ServerApp('test', factory.make_server())

    server_app.resolve_action(Action.play('1111', '111').json())
    server_app.resolve_action(Action.flip('1111').json())

    server_app.resolve_action(Action.play('3333', '222').json())
    server_app.resolve_action(Action.flip('3333').json())
    server_app.resolve_action(Action.attack('3333', '1111').json())

    client_game = GameData.from_server(server_app.game, 'A').make_client()

    defender = client_game.board.lanes[0].sides[0].cards[0]
    assert defender.card_id == '1111'
    assert defender.value == 'A'
    assert defender.minion.hp == 1

    attacker = client_game.board.lanes[0].sides[1].cards[0]
    assert attacker.card_id == '3333'
    assert attacker.value == '3'
    assert attacker.minion.hp == 2

