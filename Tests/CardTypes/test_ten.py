import pytest

from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_ten():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('X_1', 'X'),
        CardData('X_2', 'X'),
        CardData('10', '10'),
    ])
    factory.with_hand('B', [
        CardData('X_3', 'X'),
        CardData('X_4', 'X'),
        CardData('X_5', 'X'),
    ])
    game = factory.make_server()

    game.play('10', '111')
    game.flip('10')

    game.play('X_3', '222')
    game.play('X_4', '222')
    game.play('X_5', '444')

    game.attack('10', ['X_3', 'X_4'])

    assert game.find_card_from_board('X_3').minion.hp == 1
    assert game.find_card_from_board('X_4').minion.hp == 1

def test_ten_with_nine():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('9', '9'),
        CardData('X', 'X'),
    ])
    factory.with_hand('B', [
        CardData('10', '10'),
    ])
    game = factory.make_server()

    game.active_player().actions = 3
    game.play('9', '111')
    game.flip('9')
    game.play('X', '111')

    game.play('10', '222')
    game.flip('10')
    with pytest.raises(Exception, match="Tried to cleave a Stealth card"):
        game.attack('10', ['X', '9'])

    game.attack('10', ['9'])

    assert game.find_card_from_board('9').minion.hp == 1
