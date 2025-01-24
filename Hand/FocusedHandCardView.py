import pygame

from Card.CardView import CardView


class FocusedHandCardView(CardView):
    zoom = 1.1

    def __init__(self, card, pos):
        self.focused = True
        super().__init__(card, pos)

    def touching_mouse(self, mouse):
        m_x, m_y = mouse
        x, y = self.position()
        w, h = self.w * self.zoom, self.h * self.zoom
        return x <= m_x <= x + w and y <= m_y <= y + h
