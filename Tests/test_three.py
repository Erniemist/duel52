from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_three():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('3333', '3'),
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

    assert game.find_card_from_board('3333') is not None
    assert not game.find_card_from_board('3333').minion.face_down
    assert '3333' not in game.graveyard.cards.keys()
