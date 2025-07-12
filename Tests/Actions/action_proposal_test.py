from Client.Actions.AttackAction import AttackAction
from Client.Actions.FlipAction import FlipAction
from Client.Actions.PlayAction import PlayAction
from DataTransfer.CardData import CardData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory


def test_no_proposals():
    factory = GameFactory()
    game = factory.make_server()

    client_game = GameData.from_server(game, 'A').make_client()

    assert client_game.proposals == []


def test_propose_play():
    factory = GameFactory()
    factory.with_hand('A', [CardData('X', 'X')])
    factory.with_hand('B', [CardData('X_2', 'X')])
    game = factory.make_server()

    client_game = GameData.from_server(game, 'A').make_client()

    expected_proposals = [{
        'action': PlayAction.name,
        'data': {'card': 'X', 'side': '111'},
    }, {
        'action': PlayAction.name,
        'data': {'card': 'X', 'side': '333'},
    }, {
        'action': PlayAction.name,
        'data': {'card': 'X', 'side': '555'},
    }]
    check_proposals(client_game, expected_proposals)


def test_propose_flip():
    factory = GameFactory()
    factory.with_hand('A', [CardData('X', 'X')])
    game = factory.make_server()
    game.play('X', '111')

    client_game = GameData.from_server(game, 'A').make_client()

    expected_proposals = [{
        'action': FlipAction.name,
        'data': {'card': 'X'},
    }]
    check_proposals(client_game, expected_proposals)


def test_propose_attack():
    factory = GameFactory()
    factory.with_hand('A', [CardData('8', '8')])
    factory.with_hand('B', [CardData('9', '9')])
    game = factory.make_server()
    game.play('8', '111')
    game.flip('8')

    game.play('9', '222')
    game.flip('9')
    game.attack('9', ['8'])

    client_game = GameData.from_server(game, 'A').make_client()

    expected_proposals = [{
        'action': AttackAction.name,
        'data': {'attacker': '8', 'targets': ['9']},
    }]
    check_proposals(client_game, expected_proposals)


def check_proposals(client_game, expected_proposals):
    assert len(expected_proposals) == len(client_game.proposals)
    for expectation in expected_proposals:
        assert any(
            expectation['action'] == proposal['action']
            and expectation['data'] == proposal['data']
            for proposal in client_game.proposals
        )
