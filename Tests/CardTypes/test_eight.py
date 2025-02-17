from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_eight():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('X_1', 'X'),
        CardData('X_2', 'X'),
        CardData('8', '8'),
    ])
    factory.with_hand('B', [
        CardData('X_3', 'X'),
        CardData('X_4', 'X'),
        CardData('X_5', 'X'),
    ])
    game = factory.make_server()

    game.play('8', '111')
    game.flip('8')

    game.active_player().actions = 6
    game.play('X_3', '222')
    game.flip('X_3')
    game.attack('X_3', ['8'])
    game.play('X_4', '222')
    game.flip('X_4')
    game.attack('X_4', ['8'])

    assert game.find_card_from_board('X_3').minion.hp == 1
    assert game.find_card_from_board('X_4').minion.hp == 1


def test_eight_with_pair():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('8', '8'),
    ])
    factory.with_hand('B', [
        CardData('X_3', 'X'),
        CardData('X_4', 'X'),
        CardData('X_5', 'X'),
    ])
    game = factory.make_server()

    game.play('8', '111')
    game.flip('8')

    game.active_player().actions = 6
    game.play('X_3', '222')
    game.flip('X_3')
    game.play('X_4', '222')
    game.flip('X_4')
    game.pair('X_3', 'X_4')
    game.attack('X_3', ['8'])

    assert game.find_card_from_board('X_3').minion.hp == 1
    assert game.find_card_from_board('X_4').minion.hp == 1
