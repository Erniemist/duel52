from Client.Cursor.Target import Target
from Server.Choices.CardChoice import CardChoice
from Server.Choices.FaceDown import FaceDown
from Server.Choices.Friendly import Friendly
from Server.Choices.FromBoard import FromBoard
from Server.Choices.FromHand import FromHand
from Server.Choices.OtherLane import OtherLane


class ChoiceData:
    def __init__(self, validators, target_source_id, target_style, optional):
        self.validators = validators
        self.target_source_id = target_source_id
        self.target_style = target_style
        self.optional = optional

    @staticmethod
    def from_server(choice):
        return ChoiceData(
            [
                (validator.name, validator.card.card_id if validator.card else None)
                for validator in choice.choice_validators
            ],
            choice.target.source_id,
            choice.target.style,
            choice.optional,
        )

    def make_client(self, player, game):
        validators = [self.make_validator(name, player, game, card) for name, card in self.validators]
        target = Target(self.target_source_id, self.target_style)
        return CardChoice(validators, game, player, target, self.optional)

    def make_validator(self, name, player, game, card_id=None):
        card = game.find_card_from_board(card_id) if card_id is not None else None
        match name:
            case FromHand.name:
                return FromHand(player)
            case FromBoard.name:
                return FromBoard(game)
            case FaceDown.name:
                return FaceDown()
            case OtherLane.name:
                return OtherLane(card)
            case Friendly.name:
                return Friendly(card)
        raise Exception(f"{name} is not a validator")

    def to_json(self):
        return {
            'validators': self.validators,
            'target_source_id': self.target_source_id,
            'target_style': self.target_style,
            'optional': self.optional,
        }

    @staticmethod
    def from_json(data):
        return ChoiceData(
            data['validators'],
            data['target_source_id'],
            data['target_style'],
            data['optional'],
        )
