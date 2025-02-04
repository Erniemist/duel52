from Server.Triggers.FlipTrigger import FlipTrigger


class Six:
    """When this card flips, freeze all enemy minions in the same lane."""
    value = '6'

    def __init__(self, card):
        self.card = card

    def handle_triggers(self, trigger):
        if (
            isinstance(trigger, FlipTrigger)
            and trigger.source_is(self.card)
        ):
            for card in self.card.host.other_side().cards:
                card.minion.frozen = True
