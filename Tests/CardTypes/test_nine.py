from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_nine_with_six():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('9_1', '9'),
        CardData('9_2', '9'),
    ])
    factory.with_hand('B', [
        CardData('6', '6'),
    ])
    game = factory.make_server()

    game.active_player().actions = 3
    game.play('9_1', '111')
    game.flip('9_1')
    game.play('9_2', '111')

    game.play('6', '222')
    game.flip('6')

    assert not game.find_card_from_board('9_1').minion.frozen
    assert game.find_card_from_board('9_2').minion.frozen

def test_nine_with_four():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('9', '9'),
    ])
    factory.with_hand('B', [
        CardData('4', '4'),
    ])
    game = factory.make_server()

    game.active_player().actions = 1
    game.play('9', '111')

    game.play('4', '222')
    game.flip('4')
    game.choose('9')

    assert len(game.player_by_team('B').known_cards) == 2

def test_nine_with_queen():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('9', 'X'),
        CardData('Q', 'Q'),
        CardData('X', 'X'),
    ])
    game = factory.make_server()

    game.play('9', '111')
    game.flip('9')
    game.play('Q', '333')
    game.flip('Q')
    game.choose('9')

    assert len(game.find_side('333').minions()) == 2
    assert game.find_card_from_board('9').minion.side.side_id == '333'
