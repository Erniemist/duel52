from Server.Choices.FromHand import FromHand
from Server.Triggers.FlipTrigger import FlipTrigger


class Two:
    """When this card flips, draw a card, then discard a card."""
    value = '2'

    def __init__(self, card):
        self.card = card

    def handle_triggers(self, trigger):
        if (
            isinstance(trigger, FlipTrigger)
            and trigger.source_is(self.card)
        ):
            trigger.player.deck.draw_from_top(trigger.player.hand)
            self.card.game.await_choice(FromHand(lambda card: card.move_to(card.game.graveyard)))
