from Client.Cursor.Target import Target
from Server.CardTypes.Abilities.OnFlip import OnFlip
from Server.Choices.CardChoice import CardChoice
from Server.Choices.FromHand import FromHand
from Server.Effects.Effect import Effect
from Server.Effects.effects import discard, draw


class Two(OnFlip):
    description = 'When this card flips, draw a card, then discard a card.'

    def __init__(self, card, game, trigger):
        player = trigger.player
        self.discard_choice = CardChoice([FromHand(player)], game, player, Target.harm(card.minion))
        super().__init__(
            [
                Effect(lambda: draw(player)),
                self.discard_choice,
                Effect(lambda: discard(game, self.discard_choice.card)),
            ],
        )
