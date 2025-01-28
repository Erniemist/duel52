import pygame.draw

from ViewObject import ViewObject


class ActionView(ViewObject):
    font_size = 30
    weight = 5

    def __init__(self, app, player, x, y):
        super().__init__(player, app, x, y, 100, 100)
        self.player = self.real

    def draw(self, screen):
        x, y = self.position()
        x -= self.w / 2
        y -= self.w / 2
        pygame.draw.ellipse(screen, (0, 0, 0), (x, y, self.w, self.w))
        pygame.draw.ellipse(
            screen,
            (255, 255, 0),
            (x + self.weight, y + self.weight, self.w - self.weight * 2, self.w - self.weight * 2)
        )
        font = pygame.font.SysFont('arial', self.font_size)
        text = font.render(str(self.player.actions), True, (0, 0, 0))

        screen.blit(text, (
            x + self.w / 2 - text.get_width() / 2,
            y + self.w / 2 - text.get_height() / 2,
        ))

