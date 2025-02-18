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
        CardData('J', 'J'),
        CardData('X_1', 'X'),
    ])
    factory.with_hand('B', [
        CardData('A', 'A'),
        CardData('X_2', 'X'),
    ])
    game = factory.make_server()

    game.active_player().actions = 3
    game.play('J', '111')
    game.flip('J')
    game.play('X_1', '111')

    game.play('A', '222')
    game.flip('A')
    with pytest.raises(Exception, match='Minion X_1 is protected by a Jack'):
        game.attack('A', ['X_1'])