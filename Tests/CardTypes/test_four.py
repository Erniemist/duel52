import pytest

from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_four():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('3333', 'X'),
    ])
    factory.with_hand('B', [
        CardData('4444', '4'),
    ])
    game = factory.make_server()
    game.active_player().actions = 3
    game.play('1111', '111')
    game.play('2222', '111')
    game.flip('2222')

    game.play('4444', '222')
    assert len(game.player_by_team('A').known_cards) == 3
    assert len(game.player_by_team('B').known_cards) == 2
    game.flip('4444')
    assert len(game.player_by_team('A').known_cards) == 4
    assert len(game.player_by_team('B').known_cards) == 2
    with pytest.raises(Exception, match=f"2222 is not a valid FaceDown choice"):
        game.choose('2222')
    game.choose('1111')
    assert len(game.player_by_team('A').known_cards) == 4
    assert len(game.player_by_team('B').known_cards) == 3
