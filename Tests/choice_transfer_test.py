from Client.Cursor.Target import Target
from DataTransfer.CardData import CardData
from DataTransfer.ChoiceData import ChoiceData
from GameFactory import GameFactory
from Server.Choices.CardChoice import CardChoice
from Server.Choices.FromHand import FromHand
from Server.ServerGameState import ServerGameState


def test_make_server():
    factory = GameFactory()
    factory.with_hand('A', [CardData('X_1', 'X'), CardData('X_2', 'X')])
    game: ServerGameState = factory.make_server()
    player = game.active_player()
    game.play('X_1', '111')
    card = game.find_card('X_1')

    server_choice = CardChoice([FromHand(player)], game, player, Target.harm(card.minion), True)

    client_choice = ChoiceData.from_server(game, server_choice).make_client(game)
    assert len(client_choice.cards) == 1
    assert client_choice.cards[0].card_id == 'X_2'
    assert client_choice.target.style == Target.RED
    assert client_choice.target.source_id == 'X_1'
    assert client_choice.optional
