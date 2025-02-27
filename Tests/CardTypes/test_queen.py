import pytest

from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_queen():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('Q', 'Q'),
        CardData('X_1', 'X'),
        CardData('X_2', 'X'),
    ])
    factory.with_hand('B', [
        CardData('X_3', 'X'),
    ])
    game = factory.make_server()
    game.play('Q', '111')
    game.play('X_1', '111')

    game.play('X_3', '444')
    game.flip('X_3')
    game.new_turn()

    game.play('X_2', '333')
    assert len(game.find_side('111').cards) == 2
    game.flip('Q')
    with pytest.raises(Exception, match='X_1 is not a valid OtherLane choice'):
        game.choose('X_1')
    with pytest.raises(Exception, match='X_3 is not a valid Friendly choice'):
        game.choose('X_3')
    game.choose('X_2')
    assert len(game.find_side('111').cards) == 3


def test_pull_pair():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('Q', 'Q'),
        CardData('X_1', 'X'),
        CardData('X_2', 'X'),
        CardData('X_3', 'X'),
    ])
    game = factory.make_server()

    game.play('Q', '111')
    game.play('X_1', '333')
    game.flip('X_1')
    game.play('X_2', '333')
    game.flip('X_2')
    game.pair('X_1', 'X_2')
    game.flip('Q')
    game.choose('X_1')
    assert len(game.find_side('111').cards) == 3
