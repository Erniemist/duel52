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
        card = self.draw_surface()
        x, y = self.position()
        x += self.w / 2
        y += self.h / 2
        card_rect = card.get_rect(center=(x, y))
        screen.blit(card, card_rect)

    def draw_surface(self):
        surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        card = self.draw_card(surface)
        return pygame.transform.rotate(card, self.rotation)

    def draw_focused_card(self, screen):
        return self.draw_card(screen)

    def draw_card(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.style,
            (0, 0, self.w, self.h),
            border_radius=self.weight
        )

        if self.face_down:
            pygame.draw.rect(
                screen,
                self.back_colour,
                (self.weight, self.weight, self.w - self.weight * 2, self.h - self.weight * 2),
                border_radius=self.weight
            )
            return screen
        pygame.draw.rect(
            screen,
            self.front_colour,
            (self.weight, self.weight, self.w - self.weight * 2, self.h - self.weight * 2),
            border_radius=self.weight
        )
        font = pygame.font.SysFont('arial', self.font_size)
        numeral = font.render(self.card.value, True, (0, 0, 0))

        screen.blit(numeral, (
            self.w / 2 - numeral.get_width() / 2,
            self.h / 2 - numeral.get_height() / 2,
        ))
        return screen
