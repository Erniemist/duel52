class Effect:
    def __init__(self, choices_required=None):
        self.choices_required = choices_required if choices_required else []
        self.resolved = False

    def _resolve(self):
        pass

    def resolve(self):
        self._resolve()
        self.resolved = True

    def choices_remaining(self):
        return any(required_choice.choice is None for required_choice in self.choices_required)

    def next_choice(self):
        return next(
            required_choice
            for required_choice in self.choices_required
            if required_choice.choice is None
        )
