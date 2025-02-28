from Client.Cursor.Target import Target
from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Choices.CardChoice import CardChoice
from Server.Choices.FaceDown import FaceDown
from Server.Choices.FromBoard import FromBoard
from Server.Effects.Effect import Effect


class Four(OnFlip):
    description = 'When this card flips, look at a facedown card.'

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
                Effect(self.peek),
            ],
        )

    def peek(self):
        if self.peek_choice.card is not None:
            self.player.learn(self.peek_choice.card)
