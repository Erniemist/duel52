import pytest

from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_jack_hp():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('J', 'J'),
    ])
    factory.with_hand('B', [
        CardData('A', 'A'),
        CardData('X_2', 'X'),
    ])
    game = factory.make_server()

    game.play('J', '111')
    game.flip('J')

    game.new_turn()
    game.play('A', '222')
    game.flip('A')
    game.attack('A', ['J'])
    game.attack('A', ['J'])
    assert len(game.find_side('111').cards) == 1


def test_jack_taunt():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('J_1', 'J'),
        CardData('J_2', 'J'),
        CardData('X_1', 'X'),
    ])
    factory.with_hand('B', [
        CardData('A', 'A'),
        CardData('X_2', 'X'),
    ])
    game = factory.make_server()

    game.active_player().actions = 5
    game.play('J_1', '111')
    game.flip('J_1')
    game.play('J_2', '111')
    game.flip('J_2')
    game.play('X_1', '111')

    game.play('A', '222')
    game.flip('A')
    with pytest.raises(Exception, match='Tried to attack a non-Jack minion'):
        game.attack('A', ['X_1'])
    game.attack('A', ['J_1'])
    assert game.find_card('J_1').minion.hp == 2
    assert game.find_card('J_2').minion.hp == 3
