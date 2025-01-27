from Deck.DeckView import DeckView
from Hand.HandView import HandView
from ViewObject import ViewObject


class PlayerView(ViewObject):
    def __init__(self, player, app, w, h):
        if player.team == app.team:
            y = h * 0.95
            flipped = False
        else:
            y = h * 0.05
            flipped = True
        super().__init__(player, app, w / 4, y)
        self.player = self.real
        hand_view = HandView(
            player.hand,
            app,
            w / 4,
            0,
            flipped=flipped,
        )
        deck_view = DeckView(player.deck, app, 0, 0)
        self.set_children([hand_view, deck_view])

