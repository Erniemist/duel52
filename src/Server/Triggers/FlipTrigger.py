from Server.Triggers.Trigger import Trigger


class FlipTrigger(Trigger):
    def __init__(self, card_id):
        super().__init__(card_id)
