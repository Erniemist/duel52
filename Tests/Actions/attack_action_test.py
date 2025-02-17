import pytest

from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory


def test_attack_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('X_1', 'X'), CardData('X_2', 'X')])
    factory.with_hand('B', [CardData('X_3', 'X'), CardData('x_4', 'X')])
    game = factory.make_server()

    game.play('X_1', '111')
    game.flip('X_1')

    game.play('X_3', '222')
    game.flip('X_3')
    game.attack('X_3', ['X_1'])

    client_game = GameData.from_server(game, 'A').make_client()

    defender = client_game.board.lanes[0].sides[0].cards[0]
    assert defender.card_id == 'X_1'
    assert defender.minion.hp == 1

    attacker = client_game.board.lanes[0].sides[1].cards[0]
    assert attacker.card_id == 'X_3'
    assert attacker.minion.hp == 2


def test_attack_validation():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('X_1', 'X'),
        CardData('X_2', 'X'),
        CardData('X_3', 'X'),
    ])
    factory.with_hand('B', [
        CardData('X_4', 'X'),
        CardData('X_5', 'X'),
        CardData('X_6', 'X'),
    ])
    game = factory.make_server()

    game.play('X_1', '111')
    game.flip('X_1')

    game.play('X_4', '222')
    game.play('X_5', '444')
    game.play('X_6', '222')

    with pytest.raises(Exception, match="Tried to attack from an enemy minion"):
        game.attack('X_4', ['X_1'])

    with pytest.raises(Exception, match="Frozen minion X_1 cannot attack"):
        game.find_card_from_board('X_1').minion.frozen = True
        game.attack('X_1', ['X_4'])
    game.find_card_from_board('X_1').minion.frozen = False

    with pytest.raises(Exception, match="Tried to attack a minion in another lane"):
        game.attack('X_1', ['X_5'])

    game.play('X_2', '111')
    with pytest.raises(Exception, match="Tried to attack a friendly minion"):
        game.attack('X_1', ['X_2'])

    with pytest.raises(Exception, match="Tried to attack with a facedown minion"):
        game.attack('X_2', ['X_4'])

    with pytest.raises(Exception, match="Tried to attack multiple minions"):
        game.attack('X_1', ['X_4', 'X_6'])

    game.attack('X_1', ['X_4'])
    with pytest.raises(Exception, match="Tried to attack with an exhausted minion"):
        game.attack('X_1', ['X_4'])
