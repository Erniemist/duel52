from functools import lru_cache

import pygame

from Client.ViewObject import ViewObject


class CardView(ViewObject):
    w = 125
    h = 175
    weight = 4
    font_size = 30
    back_colour = (230, 100, 100)
    back_colour_frozen = (200, 70, 125)
    front_colour = (230, 230, 230)
    front_colour_frozen = (200, 200, 255)
    highlight = (255, 255, 0)
    normal = (0, 0, 0)

    def __init__(self, card, app, pos, rotation=0, face_down=False, w=125, h=175, style=None):
        x, y = pos
        super().__init__(card, app, x, y, w, h)
        self.card = self.real
        self.rotation = rotation
        self.face_down = face_down
        self.style = self.normal if style is None else style

    def draw(self, screen: pygame.Surface):
        card = make_image(self.style, self.face_down, self.card.value, self.w, self.h, self.rotation)
        x, y = self.position()
        x += self.w / 2
        y += self.h / 2
        card_rect = card.get_rect(center=(x, y))
        screen.blit(card, card_rect)

@lru_cache()
def make_image(style, face_down, value, w, h, rotation):
    surface = pygame.Surface((w, h), pygame.SRCALPHA)
    card = draw_card(style, face_down, value, w, h, surface)
    return pygame.transform.rotate(card, rotation)

def draw_card(style, face_down, value, w, h, screen: pygame.Surface):
    pygame.draw.rect(
        screen,
        style,
        (0, 0, w, h),
        border_radius=CardView.weight
    )

    if face_down:
        pygame.draw.rect(
            screen,
            CardView.back_colour,
            (CardView.weight, CardView.weight, w - CardView.weight * 2, h - CardView.weight * 2),
            border_radius=CardView.weight
        )
        return screen
    pygame.draw.rect(
        screen,
        CardView.front_colour,
        (CardView.weight, CardView.weight, w - CardView.weight * 2, h - CardView.weight * 2),
        border_radius=CardView.weight
    )
    font = pygame.font.SysFont('arial', CardView.font_size)
    numeral = font.render(value, True, (0, 0, 0))

    screen.blit(numeral, (
        w / 2 - numeral.get_width() / 2,
        h / 2 - numeral.get_height() / 2,
    ))
    return screen
