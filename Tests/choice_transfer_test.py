from copy import deepcopy

from Client.Cursor.Target import Target
from DataTransfer.CardData import CardData
from DataTransfer.ChoiceData import ChoiceData
from DataTransfer.GameData import GameData
from GameFactory import GameFactory
from Server.Choices.CardChoice import CardChoice
from Server.Choices.FromHand import FromHand
from Server.Choices.Validator import Validator
from Server.ServerGameState import ServerGameState


def test_make_server():
    factory = GameFactory()
    factory.with_hand('A', [CardData('X_1', 'X')])
    game: ServerGameState = factory.make_server()
    player = game.active_player()
    game.play('X_1', '111')
    card = game.find_card('X_1')

    server_choice = CardChoice([FromHand(player)], game, player, Target.harm(card.minion), True)

    client_choice: CardChoice = ChoiceData.from_server(server_choice).make_client(player, game)
    assert client_choice.chooser.team == 'A'
    assert client_choice.card is None
    assert client_choice.target.style == Target.RED
    assert client_choice.target.source_id == 'X_1'
    assert client_choice.optional
    validators = client_choice.choice_validators
    assert len(validators) == 1
    validator: Validator = validators[0]
    assert validator.name == FromHand.name
    assert validator.card is None


def test_json():
    factory = GameFactory()
    factory.with_hand('A', [CardData('X_1', 'X')])
    game: ServerGameState = factory.make_server()
    player = game.active_player()
    game.play('X_1', '111')
    card = game.find_card('X_1')

    server_choice = CardChoice([FromHand(player)], game, player, Target.harm(card.minion), True)

    choice_json = ChoiceData.from_server(server_choice).to_json()
    client_choice: CardChoice = ChoiceData.from_json(choice_json).make_client(player, game)
    assert client_choice.chooser.team == 'A'
    assert client_choice.card is None
    assert client_choice.target.style == Target.RED
    assert client_choice.target.source_id == 'X_1'
    assert client_choice.optional
    validators = client_choice.choice_validators
    assert len(validators) == 1
    validator: Validator = validators[0]
    assert validator.name == FromHand.name
    assert validator.card is None
