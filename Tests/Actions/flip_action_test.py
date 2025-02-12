import pytest

from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory


def test_flip_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('1111', 'A'), CardData('2222', '2')])
    factory.with_hand('B', [CardData('3333', '3'), CardData('4444', '4')])
    game = factory.make_server()
    game.play('1111', '111')
    game.flip('1111')
    client_game_1 = GameData.from_server(game, 'A').make_client()

    card = client_game_1.board.lanes[0].sides[0].cards[0]
    assert card.card_id == '1111'
    assert card.value == 'A'

    client_game_2 = GameData.from_server(game, 'B').make_client()
    card = client_game_2.board.lanes[0].sides[0].cards[0]
    assert card.card_id == '1111'
    assert card.value == 'A'


def test_flip_validation():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('3333', 'X'),
    ])
    factory.with_hand('B', [
        CardData('4444', 'X'),
        CardData('5555', 'X'),
    ])
    game = factory.make_server()

    game.play('1111', '111')
    game.new_turn()

    game.play('4444', '222')
    game.new_turn()

    with pytest.raises(Exception, match="Minion 4444 is not on your board"):
        game.flip('4444')

    with pytest.raises(Exception, match="Frozen minion 1111 cannot flip"):
        game.find_card_from_board('1111').minion.frozen = True
        game.flip('1111')

    game.find_card_from_board('1111').minion.frozen = False
    game.flip('1111')

    with pytest.raises(Exception, match="Faceup minion 1111 cannot flip"):
        game.flip('1111')
