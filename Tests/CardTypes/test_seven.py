from DataTransfer.CardData import CardData
from GameFactory import GameFactory


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
    game = factory.make_server()

    game.play('1111', '111')
    game.play('7777', '111')

    game.play('4444', '222')
    game.flip('4444')
    game.attack('4444', ['1111'])

    game.flip('1111')
    game.attack('1111', ['4444'])
    game.play('2222', '333')

    game.play('3333', '444')
    game.flip('3333')
    game.attack('3333', ['2222'])

    game.flip('7777')

    assert game.find_card_from_board('1111').minion.hp == 2
    assert game.find_card_from_board('2222').minion.hp == 2
    assert game.find_card_from_board('7777').minion.hp == 2

    assert game.find_card_from_board('4444').minion.hp == 1
