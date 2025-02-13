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

    game.play('X_3', '222')
    game.flip('X_3')
    game.attack('X_3', '8')

    assert game.find_card_from_board('X_3').minion.hp == 1
    assert game.find_card_from_board('8').minion.hp == 1
