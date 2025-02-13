from Client.Cursor.Target import Target
from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.CardTypes.CardType import CardType
from Server.Choices.CardChoice import CardChoice
from Server.Choices.FaceDown import FaceDown
from Server.Choices.FromBoard import FromBoard
from Server.Effects.Effect import Effect


class Four(CardType):
    """When this card flips, look at a facedown card."""
    value = '4'

    class Ability(OnFlip):
        def __init__(self, card, game, trigger):
            self.player = trigger.player
            self.peek_choice = CardChoice(
                [FromBoard(game), FaceDown()],
                game,
                self.player,
                Target.affect(card.minion),
            )
            super().__init__(
                [
                    self.peek_choice,
                    Effect(lambda: self.player.learn(self.peek_choice.card)),
                ],
            )

    def __init__(self, card):
        super().__init__(card, abilities=[self.Ability])
