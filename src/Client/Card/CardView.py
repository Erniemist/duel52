import pygame

from Client.Card.CardImage import CardImage
from Client.ViewObject import ViewObject


class CardView(ViewObject):
    def __init__(self, card, app, pos, style, w=None, h=None):
        x, y = pos
        super().__init__(
            card,
            app,
            x,
            y,
            w=w if w is not None else CardImage.w,
            h=h if h is not None else CardImage.h,
        )
        self.card = self.real
        self.style = style

    def draw(self, screen: pygame.Surface):
        x, y = self.position()
        x += self.w / 2
        y += self.h / 2
        card = self.image()
        card_rect = card.get_rect(center=(x, y))
        screen.blit(card, card_rect)

    def image(self):
        raise NotImplementedError()
