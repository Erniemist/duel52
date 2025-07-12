from functools import lru_cache

import pygame.draw

from Client.ViewObject import ViewObject


class ActionView(ViewObject):
    font_size = 30
    weight = 5

    def __init__(self, app, player, x, y):
        w = 100
        super().__init__(player, app, x - w / 2, y - w / 2, w=w, h=w)
        self.player = self.real

    def draw(self, screen):
        screen.blit(
            self.get_image(self.player.actions, self.font_size, self.w, self.weight),
            self.position(),
        )

    @staticmethod
    @lru_cache()
    def get_image(actions, font_size, w, weight):
        surface = pygame.Surface((w, w), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (0, 0, 0), (0, 0, w, w))
        pygame.draw.ellipse(
            surface,
            (255, 255, 0),
            (weight, weight, w - weight * 2, w - weight * 2)
        )
        font = pygame.font.SysFont('arial', font_size)
        text = font.render(str(actions), True, (0, 0, 0))
        surface.blit(text, (
            w / 2 - text.get_width() / 2,
            w / 2 - text.get_height() / 2,
        ))
        return surface

