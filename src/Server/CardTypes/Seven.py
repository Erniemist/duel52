from Server.Triggers.FlipTrigger import FlipTrigger


class Seven:
    """When this card flips, heal ALL friendly minions."""
    value = '7'

    def __init__(self, card):
        self.card = card

    def handle_triggers(self, trigger):
        if (
            isinstance(trigger, FlipTrigger)
            and trigger.source_is(self.card)
        ):
            for minion in self.card.minion.player.minions():
                minion.hp = minion.max_hp
