from Server.Ability import Ability
from Server.Triggers.FlipTrigger import FlipTrigger


class OnFlip(Ability):
    @staticmethod
    def should_trigger(card, trigger):
        return isinstance(trigger, FlipTrigger) and trigger.source_is(card)
