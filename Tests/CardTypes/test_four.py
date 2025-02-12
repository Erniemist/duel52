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
    game.play('1111', '111')
    game.play('2222', '111')

    game.play('4444', '222')
    assert len(game.player_by_team('A').known_cards) == 3
    assert len(game.player_by_team('B').known_cards) == 1
    game.flip('4444')
    assert len(game.player_by_team('A').known_cards) == 4
    assert len(game.player_by_team('B').known_cards) == 1
    game.choose('1111')
    assert len(game.player_by_team('A').known_cards) == 4
    assert len(game.player_by_team('B').known_cards) == 2
