from Server.Triggers.FlipTrigger import FlipTrigger


class Seven:
    """When this card flips, heal all friendly minions in the same lane."""
    value = '7'

    def __init__(self, card):
        self.card = card

    def handle_triggers(self, trigger):
        if (
            isinstance(trigger, FlipTrigger)
            and trigger.source_is(self.card)
        ):
            for card in self.card.host.cards:
                card.minion.hp = card.minion.max_hp
