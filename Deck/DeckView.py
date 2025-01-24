import pygame

from Card.CardView import CardView
from ViewObject import ViewObject


class DeckView(ViewObject):
    w = 125
    h = 175

    def __init__(self, deck, x, y):
        super().__init__(deck, x, y - self.h / 2, self.w, self.h)
        self.deck = self.real

    def draw(self, screen: pygame.Surface):
        x, y = self.position()
        border_colour = (255, 255, 0) if self.focused else (0, 0, 0)
        margin = 5
        pygame.draw.rect(screen, border_colour, (x, y, self.w, self.h), border_radius=margin)
        pygame.draw.rect(
            screen,
            CardView.back_colour,
            (x + margin, y + margin, self.w - margin * 2, self.h - margin * 2),
            border_radius=margin
        )

