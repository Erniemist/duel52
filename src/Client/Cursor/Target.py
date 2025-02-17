class Target:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (100, 100, 255)

    def __init__(self, source_id, style):
        self.source_id = source_id
        self.style = style

    @staticmethod
    def harm(source):
        return Target(source.card.card_id, Target.RED)

    @staticmethod
    def buff(source):
        return Target(source.card.card_id, Target.GREEN)

    @staticmethod
    def affect(source):
        return Target(source.card.card_id, Target.BLUE)
