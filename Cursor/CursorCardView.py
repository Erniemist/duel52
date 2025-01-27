import pygame

from Card.CardView import CardView


class CursorCardView(CardView):
    shadow_scale = 1.1
    shadow_offset = (20, 20)
    perspective_scale = 1.1

    def __init__(self, card, app, pos):
        super().__init__(card, app, pos)

    def draw_surface(self):
        x, y = self.shadow_offset
        w = self.w * self.shadow_scale + x
        h = self.h * self.shadow_scale + y
        card = pygame.Surface((w, h), pygame.SRCALPHA)
        shadow = self.draw_shadow()
        card.blit(shadow, self.shadow_offset)
        card = self.draw_focused_card(card)
        return pygame.transform.scale(card, (w * self.perspective_scale, h * self.perspective_scale))

    def draw_shadow(self):
        shadow = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            (0, 0, 0, 80),
            (0, 0, self.w, self.h),
            border_radius=self.weight,
        )
        return pygame.transform.scale(shadow, (self.w * self.shadow_scale, self.h * self.shadow_scale))

    def on_mouse_move(self):
        self.card.x, self.card.y = self.app.cursor.position
