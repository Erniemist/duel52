from Client.Cursor.Target import Target
from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Choices.CardChoice import CardChoice
from Server.Choices.Friendly import Friendly
from Server.Choices.FromBoard import FromBoard
from Server.Choices.OtherLane import OtherLane
from Server.Effects.Effect import Effect


class Queen(OnFlip):
    description = 'When this card flips, you may move a friendly card to this lane.'

    def __init__(self, card, game, trigger):
        self.card = card
        self.summons = CardChoice(
            [FromBoard(game), OtherLane(card), Friendly(card)],
            game,
            trigger.player,
            Target.affect(card.minion),
        )
        super().__init__(
            [
                self.summons,
                Effect(lambda: self.summons.card.move_to(self.card.minion.side)),
            ],
        )
