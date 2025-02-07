from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_two():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', '2'),
        CardData('3333', 'X'),
    ])
    factory.with_deck('A', [
        CardData('5555', 'X'),
        CardData('6666', 'X'),
    ])
    game = factory.make_server()
    game.active_player().actions = 3
    game.play('2222', '111')
    game.flip('2222')
    assert len(game.player_by_team('A').hand.cards) == 3
    assert len(game.player_by_team('A').deck.cards) == 1
    game.choose('1111')
    assert game.player_by_team('A').actions == 1
    assert len(game.player_by_team('A').hand.cards) == 2
    assert len(game.graveyard.cards) == 1
