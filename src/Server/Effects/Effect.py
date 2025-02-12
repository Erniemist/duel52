class Effect:
    def __init__(self, callback=None):
        self.callback = callback
        self.resolved = False

    def resolve(self):
        self.callback()
        self.resolved = True
