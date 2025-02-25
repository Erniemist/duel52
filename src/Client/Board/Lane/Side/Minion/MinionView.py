import pygame


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Client.Board.Lane.Side.Pair.PairView import PairView
from Client.Card.CardView import CardView
from Client.ViewObject import ViewObject


class MinionView(ViewObject):
    w = 125
    h = 125
    weight = 5
    font_size = 30
    highlight = (255, 255, 0)
    targeted = (255, 0, 0)
    normal = (0, 0, 0)
    exahusted_colour = (200, 200, 200)

    def __init__(self, minion, app, position):
        x, y = position
        super().__init__(minion, app, x, y, self.w, self.h)
        self.parent: None | MinionView | PairView
        self.minion = self.real
        self.minion.view_object = self
        self.border_colour = self.normal
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
        if self.minion.card.card_id in self.app.my_player().known_cards:
            font = pygame.font.SysFont('arial', self.font_size)
            numeral = font.render(self.minion.card.value, True, (0, 0, 0))

            screen.blit(numeral, (
                self.w / 2 - numeral.get_width() / 2,
                self.h / 2 - numeral.get_height() / 2,
            ))
        return screen

    def get_centre(self):
        x, y = self.position()
        return x + self.w / 2, y + self.h / 2

    def main_colour(self):
        if self.minion.face_down:
            if self.minion.frozen:
                return CardView.back_colour_frozen
            return CardView.back_colour
        if self.minion.frozen:
            return CardView.front_colour_frozen
        if self.minion.attacks_left() > 0:
            return CardView.front_colour
        return self.exahusted_colour

    def get_border(self):
        source = self.app.cursor.target_source()
        if source and source is not self.minion and self.focused:
            return self.app.cursor.targetter.style
        if self.focused or source is self.minion or (self.minion.pair and source is self.minion.pair):
            return self.highlight
        return self.normal

    def source_of_pairing(self):
        other_pair = self.app.focused_object()
        if not other_pair:
            return False
        if not isinstance(other_pair, MinionView):
            return False
        if other_pair.minion is self.minion:
            return False
        return other_pair.minion.team == self.minion.team
