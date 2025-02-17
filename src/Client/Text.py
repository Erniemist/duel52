import pygame.font

from Client.ViewObject import ViewObject


class Text(ViewObject):
    def __init__(self, app, text, x, y, size):
        self.text = text
        self.size = size
        self.back_font = pygame.font.SysFont('Arial', size=size, bold=True)
        self.front_font = pygame.font.SysFont('Arial', size=int(size * 0.8), bold=True)
        super().__init__(real=None, app=app, x=x, y=y)

    def draw(self, screen):
        x, y = self.position()
        text = self.back_font.render(self.text, True, (255, 255, 255), (0, 0, 0))
        screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
