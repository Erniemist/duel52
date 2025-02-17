import math

from Client.Card.CardView import CardView
from Client.Hand.FocusedHandCardView import FocusedHandCardView
from Client.Hand.HandCardView import HandCardView
from Client.ViewObject import ViewObject


class HandView(ViewObject):
    squish = 0.75
    card_w = CardView.w * squish

    def __init__(self, hand, app, x, y, flipped):
        self.cards_to_show = [card for card in hand.cards if card is not app.cursor.card()]
        w = self.card_w * len(self.cards_to_show)
        super().__init__(
            hand,
            app,
            x - w / 2,
            y - CardView.h / 2,
            w,
            CardView.h,
        )
        self.flipped = flipped
        self.hand = self.real
        self.card_views = self.generate_cards()
        self.set_children(self.card_views)

    def generate_cards(self):
        cards: list[CardView] = []
        for i, card in enumerate(self.cards_to_show):
            rotation = self.card_rotation(i)
            y = self.card_y(rotation)
            if self.flipped:
                rotation *= -1
                y *= -1
            if self.card_is_focused(card):
                cards.append(FocusedHandCardView(
                    card,
                    self.app,
                    (self.card_x(i) - CardView.w * (1 - self.squish) / 4, -CardView.h * 0.5 * (-1 if self.flipped else 1)),
                    face_down=self.flipped,
                ))
            else:
                cards.append(HandCardView(
                    card,
                    self.app,
                    self,
                    i,
                    (self.card_x(i), y),
                    rotation=rotation,
                    face_down=self.flipped,
                ))
        return cards

    def card_is_focused(self, card):
        focused = self.app.focused_object()
        return focused and isinstance(focused, CardView) and focused.real.card_id == card.card_id

    def card_x(self, i):
        return i * self.card_w - CardView.w * (1 - self.squish) / 2

    def card_y(self, rotation):
        if len(self.cards_to_show) == 1:
            return 0
        return self.h * 0.255 - math.sin((90 - rotation * 2) / 180 * math.pi) * self.h / 2

    def card_rotation(self, i):
        if len(self.cards_to_show) == 1:
            return 0
        spread = 60
        return spread / 2 - spread / (len(self.cards_to_show) - 1) * i
