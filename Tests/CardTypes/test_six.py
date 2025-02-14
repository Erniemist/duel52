import pytest

from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_six_freezes():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('6666', '6'),
    ])
    factory.with_hand('B', [
        CardData('3333', 'X'),
        CardData('4444', 'X'),
        CardData('5555', 'X'),
    ])
    game = factory.make_server()

    game.play('6666', '111')

    game.new_turn()
    game.play('3333', '222')
    game.play('4444', '222')
    game.flip('4444')

    game.flip('6666')

    game.new_turn()
    game.play('5555', '222')
    game.flip('5555')

    with pytest.raises(Exception, match='Frozen minion 3333 cannot flip'):
        game.flip('3333')
    with pytest.raises(Exception, match='Frozen minion 4444 cannot attack'):
        game.attack('4444', ['6666'])
    with pytest.raises(Exception, match='Frozen minion 4444 cannot pair'):
        game.pair('4444', '5555')
    with pytest.raises(Exception, match='Frozen minion 4444 cannot pair'):
        game.pair('5555', '4444')


def test_six_wears_off():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('6666', '6'),
    ])
    factory.with_hand('B', [
        CardData('3333', 'X'),
        CardData('4444', 'X'),
        CardData('5555', 'X'),
    ])
    game = factory.make_server()

    game.play('6666', '111')

    game.new_turn()
    game.play('3333', '222')

    game.new_turn()
    game.flip('6666')

    game.new_turn()
    game.new_turn()
    game.new_turn()
    game.flip('3333')
    assert not game.find_card_from_board('3333').minion.face_down
