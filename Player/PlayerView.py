from Deck.DeckView import DeckView
from Hand.HandView import HandView
from Player.ActionView import ActionView
from ViewObject import ViewObject


class PlayerView(ViewObject):
    def __init__(self, player, app, w, h):
        top_position = h * 0.03
        bottom_position = h - top_position
        if player.team == app.team:
            y = bottom_position
            flipped = False
        else:
            y = top_position
            flipped = True
        super().__init__(player, app, w / 4, y)
        self.player = self.real
        self.set_children([
            HandView(player.hand, app, w / 4, 0, flipped=flipped),
            DeckView(player.deck, app, 0, 0),
            ActionView(app, player, w * 0.65, 50 * (1 if flipped else -1)),
        ])
