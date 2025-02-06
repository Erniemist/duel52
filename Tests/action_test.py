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


def test_attack_card():
    factory = GameFactory()
    factory.with_hand('A', [CardData('1111', 'A'), CardData('2222', '2')])
    factory.with_hand('B', [CardData('3333', '3'), CardData('4444', '4')])
    game = factory.make_server()

    game.play('1111', '111')
    game.flip('1111')

    game.play('3333', '222')
    game.flip('3333')
    game.attack('3333', '1111')

    client_game = GameData.from_server(game, 'A').make_client()

    defender = client_game.board.lanes[0].sides[0].cards[0]
    assert defender.card_id == '1111'
    assert defender.value == 'A'
    assert defender.minion.hp == 1

    attacker = client_game.board.lanes[0].sides[1].cards[0]
    assert attacker.card_id == '3333'
    assert attacker.value == '3'
    assert attacker.minion.hp == 2


def test_pair_cards():
    factory = GameFactory()
    factory.with_hand('A', [CardData('1111', 'A'), CardData('2222', 'A')])
    game = factory.make_server()

    game.play('1111', '111')
    game.play('2222', '111')
    game.flip('1111')
    game.flip('2222')
    game.pair('1111', '2222')

    client_game = GameData.from_server(game, 'A').make_client()

    minion_1 = client_game.board.lanes[0].sides[0].cards[0].minion
    minion_2 = client_game.board.lanes[0].sides[0].cards[1].minion
    assert minion_1.pair is minion_2
    assert minion_2.pair is minion_1


def test_death():
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
    game.play('3333', '111')

    game.play('4444', '222')
    game.flip('4444')
    game.attack('4444', '3333')

    game.flip('1111')
    game.play('2222', '111')
    game.flip('2222')

    game.attack('4444', '3333')

    client_game = GameData.from_server(game, 'A').make_client()

    assert client_game.find_card_from_board('3333') is None
    assert '3333' in client_game.graveyard.cards.keys()
    assert client_game.graveyard.cards['3333'].minion is None
