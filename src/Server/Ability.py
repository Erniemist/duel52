class Ability:
    def __init__(self, parts):
        self.parts = parts

    def unresolved_parts(self):
        for part in self.parts:
            if not part.resolved:
                yield part
