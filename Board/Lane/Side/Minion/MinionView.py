import pygame

import rectangle
from Card.CardView import CardView
from ViewObject import ViewObject


class MinionView(ViewObject):
    w = 125
    h = 125
    weight = 5
    font_size = 30
    highlight = (255, 255, 0)
    targeted = (255, 0, 0)
    normal = (0, 0, 0)

    def __init__(self, minion, position, rotation):
        super().__init__(minion, *position, self.w, self.h)
        self.minion = self.real
        self.rotation = rotation

    def draw(self, screen: pygame.Surface):
        minion = self.draw_surface()
        x, y = self.position()
        x += self.w / 2
        y += self.h / 2
        minion_rect = minion.get_rect(center=(x, y))
        screen.blit(minion, minion_rect)

    def draw_surface(self):
        surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        minion = self.draw_minion(surface)
        return pygame.transform.rotate(minion, self.rotation)

    def draw_minion(self, screen: pygame.Surface):
        font = pygame.font.SysFont('arial', self.font_size)
        pygame.draw.rect(
            screen,
            self.get_border(),
            (0, 0, self.w, self.h),
            border_radius=self.weight
        )
        if self.minion.face_down:
            colour = CardView.back_colour
        else:
            colour = CardView.front_colour
        pygame.draw.rect(
            screen,
            colour,
            (self.weight, self.weight, self.w - self.weight * 2, self.h - self.weight * 2),
            border_radius=self.weight
        )
        if not self.minion.face_down:
            numeral = font.render(self.minion.card.value, True, (0, 0, 0))

            screen.blit(numeral, (
                self.w / 2 - numeral.get_width() / 2,
                self.h / 2 - numeral.get_height() / 2,
            ))
        return screen

    def get_border(self):
        source = self.minion.game.cursor.target_source
        if source and source is not self.real and self.focused:
            return self.targeted
        if source is self.real or self.focused:
            return self.highlight
        return self.normal
