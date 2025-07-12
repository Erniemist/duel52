import pygame

from Client.Card.CardImage import CardImage
from Client.Card.CardView import CardView


class HandCardView(CardView):
    def __init__(self, card, app, hand, i, pos, rotation, face_down=False):
        self.hand = hand
        self.i = i
        super().__init__(card, app, pos, CardImage.normal)
        self.rotation = rotation
        self.face_down = face_down

    def image(self):
        return CardImage.make_image(self.style, self.face_down, self.card.value, self.w, self.h, self.rotation)
