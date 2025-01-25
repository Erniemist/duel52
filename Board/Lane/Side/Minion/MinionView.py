import pygame

from Board.Lane.Side.Minion.Minion import Minion
from Card.CardView import CardView
from ViewObject import ViewObject


class MinionView(ViewObject):
    w = 125
    h = 125
    weight = 5
    font_size = 30
    highlight = (255, 255, 0)
    targeted = (255, 0, 0)
    pairing = (100, 100, 255)
    normal = (0, 0, 0)
    exahusted_colour = (200, 200, 200)

    def __init__(self, minion, position):
        super().__init__(minion, *position, self.w, self.h)
        self.minion = self.real
        self.minion.view_object = self
        self.border_colour = None
        damage = minion.max_hp - minion.hp
        self.rotation = -90 / minion.max_hp * damage

    def draw(self, screen: pygame.Surface):
        self.border_colour = self.get_border()
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
            self.border_colour,
            (0, 0, self.w, self.h),
            border_radius=self.weight
        )
        pygame.draw.rect(
            screen,
            self.main_colour(),
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

    def get_centre(self):
        if self.minion.pair:
            return self.get_centre_pair()
        return self.get_centre_alone()

    def get_centre_pair(self):
        x1, y1 = self.get_centre_alone()
        x2, y2 = self.minion.pair.view_object.get_centre_alone()
        return (x1 + x2) / 2, (y1 + y2) / 2

    def get_centre_alone(self):
        x, y = self.position()
        return x + self.w / 2, y + self.h / 2

    def main_colour(self):
        if self.minion.face_down:
            colour = CardView.back_colour
        else:
            if self.minion.attacks_left() > 0:
                colour = CardView.front_colour
            else:
                colour = self.exahusted_colour
        return colour

    def get_border(self):
        source = self.minion.game.cursor.target_source
        if source and source is not self.minion and self.focused:
            if source.team != self.minion.team:
                return self.targeted
            return self.pairing
        if self.minion.pair:
            if source is self.minion or source is self.minion.pair:
                return self.highlight
        else:
            if source is self.minion:
                if self.source_of_pairing():
                    return self.pairing
                else:
                    return self.highlight
        if self.focused:
            return self.highlight
        return self.normal

    def source_of_pairing(self):
        other_pair = self.minion.game.last_focused
        if not other_pair:
            return False
        if not isinstance(other_pair, MinionView):
            return False
        if other_pair.minion is self.minion:
            return False
        return other_pair.minion.team == self.minion.team
