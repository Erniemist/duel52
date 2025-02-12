from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory


def test_attack_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('X_1', 'X'), CardData('X_2', 'X')])
    factory.with_hand('B', [CardData('X_3', 'X'), CardData('x_4', 'X')])
    game = factory.make_server()

    game.play('X_1', '111')
    game.flip('X_1')

    game.play('X_3', '222')
    game.flip('X_3')
    game.attack('X_3', 'X_1')

    client_game = GameData.from_server(game, 'A').make_client()

    defender = client_game.board.lanes[0].sides[0].cards[0]
    assert defender.card_id == 'X_1'
    assert defender.minion.hp == 1

    attacker = client_game.board.lanes[0].sides[1].cards[0]
    assert attacker.card_id == 'X_3'
    assert attacker.minion.hp == 2


def test_pair_cards():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('3333', 'X'),
    ])
    game = factory.make_server()

    game.play('1111', '111')
    game.play('2222', '111')
    game.flip('1111')
    game.flip('2222')
    game.pair('1111', '2222')

    client_game = GameData.from_server(game, 'A').make_client()

    minion_1 = client_game.board.lanes[0].sides[0].cards[0].minion
    minion_2 = client_game.board.lanes[0].sides[0].cards[1].minion
    assert minion_1.pair is minion_2
    assert minion_2.pair is minion_1


def test_death():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('3333', 'X'),
    ])
    factory.with_hand('B', [
        CardData('4444', 'X'),
        CardData('5555', 'X'),
    ])
    game = factory.make_server()

    game.play('1111', '111')
    game.play('3333', '111')

    game.play('4444', '222')
    game.flip('4444')
    game.attack('4444', '3333')

    game.flip('1111')
    game.play('2222', '111')
    game.flip('2222')

    game.attack('4444', '3333')

    client_game = GameData.from_server(game, 'A').make_client()

    assert client_game.find_card_from_board('3333') is None
    assert '3333' in client_game.graveyard.cards.keys()
    assert client_game.graveyard.cards['3333'].minion is None
