from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_nine():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('9_1', '9'),
        CardData('9_2', '9'),
    ])
    factory.with_hand('B', [
        CardData('6', '6'),
    ])
    game = factory.make_server()

    game.active_player().actions = 3
    game.play('9_1', '111')
    game.flip('9_1')
    game.play('9_2', '111')

    game.play('6', '222')
    game.flip('6')

    assert not game.find_card_from_board('9_1').minion.frozen
    assert game.find_card_from_board('9_1').minion.frozen
