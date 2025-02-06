import pytest

from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory


def test_play_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('1234', '6')])
    game = factory.make_server()
    game.play('1234', '111')
    client_game_1 = GameData.from_server(game, 'A').make_client()

    assert len(client_game_1.players[0].hand.cards) == 0
    played_card = client_game_1.board.lanes[0].sides[0].cards[0]
    assert played_card.card_id == '1234'
    assert played_card.value == '6'
    assert played_card.minion is not None
    assert played_card.minion.team == 'A'
    assert played_card.minion.hp == 2
    assert played_card.minion.attacks_made == 0

    client_game_2 = GameData.from_server(game, 'B').make_client()
    played_card = client_game_2.board.lanes[0].sides[0].cards[0]
    assert played_card.card_id == '1234'
    assert played_card.value == ''
    assert played_card.minion is not None
    assert played_card.minion.team == 'A'
    assert played_card.minion.hp == 2
    assert played_card.minion.attacks_made == 0


def test_play_validation():
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

    with pytest.raises(Exception, match="Can't play card 1111 to enemy side 222"):
        game.play('1111', '222')

    with pytest.raises(Exception, match="Card 4444 is not in hand to play"):
        game.play('4444', '111')

