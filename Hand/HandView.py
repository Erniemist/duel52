import math

from Card.CardView import CardView
from Hand.FocusedHandCardView import FocusedHandCardView
from Hand.HandCardView import HandCardView
from ViewObject import ViewObject


class HandView(ViewObject):
    card_w = CardView.w * 0.8

    def __init__(self, hand, x, y, flipped):
        w = self.card_w * len(hand.cards)
        super().__init__(hand, x - w / 2, y - CardView.h / 2, w, CardView.h)
        self.flipped = flipped
        self.hand = self.real
        self.cards = self.generate_cards()
        self.set_children(self.cards)

    def generate_cards(self):
        cards = []
        for i, card in enumerate(self.hand.cards):
            rotation = self.card_rotation(i)
            y = self.card_y(rotation)
            if self.flipped:
                rotation *= -1
                y *= -1
            cards.append(HandCardView(
                card,
                self,
                i,
                (self.card_x(i), y),
                rotation=rotation,
                facedown=self.flipped,
            ))
        return cards

    def card_x(self, i):
        return i * self.card_w

    def card_y(self, rotation):
        if len(self.hand.cards) == 1:
            return 0
        return self.h * 0.255 - math.sin((90 - rotation * 2) / 180 * math.pi) * self.h / 2

    def card_rotation(self, i):
        if len(self.hand.cards) == 1:
            return 0
        spread = 60
        return spread / 2 - spread / (len(self.hand.cards) - 1) * i

    def focus_card(self, card: HandCardView):
        focused = FocusedHandCardView(card.card, (self.card_x(card.i), -CardView.h * 0.5))
        focused.parent = self
        self.cards[card.i] = focused
        return focused
