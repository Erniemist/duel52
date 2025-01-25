import pygame

import rectangle
from Card.CardView import CardView


class FocusedHandCardView(CardView):
    zoom = 1.1

    def __init__(self, card, game, pos, face_down=False):
        self.focused = True
        super().__init__(card, game, pos, face_down=face_down, w=CardView.w * self.zoom, h=CardView.h * self.zoom)

    def touching_mouse(self):
        return rectangle.point_inside(self.game.cursor.position, (*self.position(), self.w, self.h * 2))
