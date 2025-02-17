import pygame

from Client.Card.CardView import CardView
from Client.ViewObject import ViewObject


class DeckView(ViewObject):
    w = 125
    h = 175
    font_size = 30

    def __init__(self, deck,app, x, y):
        super().__init__(deck,app, x, y - self.h / 2, self.w, self.h)
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
        if self.touching_mouse():
            font = pygame.font.SysFont('arial', self.font_size)
            numeral = font.render(str(len(self.deck.cards)), True, (255, 255, 255))

            screen.blit(numeral, (
                x + self.w / 2 - numeral.get_width() / 2,
                y + self.h / 2 - numeral.get_height() / 2,
            ))

