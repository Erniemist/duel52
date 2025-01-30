from Triggers.DeathTrigger import DeathTrigger


class Three:
    """When this card dies face down, return it to its lane face up."""
    value = '3'

    def __init__(self, card):
        self.card = card

    def handle_triggers(self, trigger):
        match trigger:
            case DeathTrigger(self.card):
                if self.card.minion.face_down:
                    self.card.move_to(self.card.minion.side)
                    self.card.minion.flip_up()
