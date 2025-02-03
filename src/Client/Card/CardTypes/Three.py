from Server.Triggers.DeathTrigger import DeathTrigger


class Three:
    """When this card dies face down, return it to its lane face up."""
    value = '3'

    def __init__(self, card):
        self.card = card

    def handle_triggers(self, trigger):
        if (
            isinstance(trigger, DeathTrigger)
            and trigger.source_is(self.card)
            and self.card.minion_last_info.face_down
        ):
            self.card.move_to(self.card.minion_last_info.side)
            self.card.minion.flip_up()
