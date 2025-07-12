from functools import lru_cache

import pygame

from Client.Card.CardImage import CardImage
from Client.ViewObject import ViewObject


class DeckView(ViewObject):
    w = 125
    h = 175
    font_size = 30

    def __init__(self, deck,app, x, y):
        super().__init__(deck,app, x, y - self.h / 2, self.w, self.h)
        self.deck = self.real

    def draw(self, screen: pygame.Surface):
        screen.blit(
            self.make_image(self.w, self.h, self.focused, self.touching_mouse(), self.font_size, len(self.deck.cards)),
            self.position(),
        )

    @staticmethod
    @lru_cache()
    def make_image(w, h, focused, touching_mouse, font_size, num_cards):
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        border_colour = (255, 255, 0) if focused else (0, 0, 0)
        margin = 5
        pygame.draw.rect(surface, border_colour, (0, 0, w, h), border_radius=margin)
        pygame.draw.rect(
            surface,
            CardImage.back_colour,
            (margin, margin, w - margin * 2, h - margin * 2),
            border_radius=margin
        )
        if touching_mouse:
            font = pygame.font.SysFont('arial', font_size)
            numeral = font.render(str(num_cards), True, (255, 255, 255))

            surface.blit(numeral, (
                w / 2 - numeral.get_width() / 2,
                h / 2 - numeral.get_height() / 2,
            ))
        return surface
