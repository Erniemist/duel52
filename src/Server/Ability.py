class Ability:
    def __init__(self, effects):
        self.effects = effects

    def unresolved_effects(self):
        for effect in self.effects:
            if not effect.resolved:
                yield effect
