from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_king():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('2_1', '2'),
        CardData('2_2', '2'),
        CardData('K', 'K'),
    ])
    factory.with_deck('A', [
        CardData('X_1', 'X'),
        CardData('X_2', 'X'),
        CardData('X_3', 'X'),
        CardData('X_4', 'X'),
        CardData('X_5', 'X'),
    ])
    game = factory.make_server()
    game.active_player().actions = 7

    assert len(game.player_by_team('A').hand.cards) == 3
    assert len(game.player_by_team('A').deck.cards) == 5
    assert len(game.graveyard.cards) == 0

    game.play('2_1', '111')
    game.flip('2_1')
    game.choose('X_1')

    assert len(game.player_by_team('A').hand.cards) == 2
    assert len(game.player_by_team('A').deck.cards) == 4
    assert len(game.graveyard.cards) == 1

    game.play('2_2', '111')
    game.flip('2_2')
    game.choose('X_2')

    assert len(game.player_by_team('A').hand.cards) == 1
    assert len(game.player_by_team('A').deck.cards) == 3
    assert len(game.graveyard.cards) == 2

    game.play('K', '111')
    game.flip('K')
    game.choose('X_3')
    game.choose('X_4')

    assert len(game.player_by_team('A').hand.cards) == 0
    assert len(game.player_by_team('A').deck.cards) == 1
    assert len(game.graveyard.cards) == 4

