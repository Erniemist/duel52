from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_ace():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('X_1', 'X'),
    ])
    factory.with_hand('B', [
        CardData('A', 'A'),
        CardData('X_2', 'X'),
    ])
    game = factory.make_server()

    game.play('X_1', '111')

    game.new_turn()
    game.play('A', '222')
    game.flip('A')
    game.attack('A', 'X_1')
    assert game.active_player().team == 'B'
    assert game.active_player().actions == 1
    game.attack('A', 'X_1')

    assert len(game.graveyard.cards) == 1
