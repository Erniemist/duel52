from DataTransfer.CardData import CardData
from GameFactory import GameFactory


def test_five():
    factory = GameFactory()
    factory.with_hand('A', [
        CardData('1111', 'X'),
        CardData('2222', 'X'),
        CardData('5555', '5'),
    ])
    game = factory.make_server()

    game.play('5555', '111')
    game.play('1111', '111')
    game.play('2222', '111')
    game.flip('5555')

    side = game.board.lanes[0].sides[0]
    assert not side.cards[0].minion.face_down
    assert not side.cards[1].minion.face_down
    assert not side.cards[2].minion.face_down
