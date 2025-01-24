class Card:
    def __init__(self, value: str, host):
        self.value = value
        self.host = host
        self.minion = None
        self.focused = False
        self.previous_host = None

    def can_select(self, game):
        if self.host == game.cursor:
            return False

        return game.active_player().team == self.host.team and game.active_player().actions > 0

    def on_select(self, game):
        game.cursor.card = self
        game.cursor.set_offset(game.focused_object)

    def move_to(self, new_host):
        self.host.remove_card(self)
        self.previous_host = self.host
        self.host = new_host
        new_host.add_card(self)
