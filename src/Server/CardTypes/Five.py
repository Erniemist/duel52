from Server.Triggers.FlipTrigger import FlipTrigger


class Five:
    """When this card flips, flip all friendly minions in the same lane."""
    value = '5'

    def __init__(self, card):
        self.card = card

    def handle_triggers(self, trigger):
        if (
            isinstance(trigger, FlipTrigger)
            and trigger.source_is(self.card)
        ):
            for card in self.card.host.cards:
                if card.minion.face_down:
                    card.minion.flip_up()
