from functools import lru_cache

import pygame

from Client.Card.CardImage import CardImage
from Client.ViewObject import ViewObject


class Header(ViewObject):
    def __init__(self, app, text, x, y):
        self.text = self.make_text(text)
        super().__init__(None, app, x, y, self.text.get_width(), self.text.get_height())

    @staticmethod
    @lru_cache()
    def make_text(text):
        font = pygame.font.SysFont('Arial', 40)
        return font.render(text, True, (0, 0, 0))

    def draw(self, screen):
        x, y = self.position()
        screen.blit(self.get_image(self.text, self.w, self.h), (x - self.w / 2, y))

    @staticmethod
    @lru_cache()
    def get_image(text, w, h):
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        surface.blit(text, (0, 0))
        return surface


class Paragraph(ViewObject):
    size = 24
    line_spacing = 2

    def __init__(self, app, paragraph, x, y, max_w):
        self.lines = self.wrap_text(paragraph, max_w)
        super().__init__(
            None,
            app,
            x,
            y,
            w=max(text.get_width() for y, text in self.lines),
            h=sum(text.get_height() for y, text in self.lines) + self.line_spacing * (len(self.lines) - 1),
        )

    @staticmethod
    @lru_cache()
    def wrap_text(paragraph, max_w):
        font = pygame.font.SysFont('Arial', 24)
        lines = []
        words = paragraph.split(' ')
        line = []
        y = 0
        for word in words:
            potential_line = line + [word]
            potential_text = Paragraph.render_line(potential_line, font)
            if potential_text.get_width() >= max_w:
                text = Paragraph.render_line(line, font)
                lines.append((y, text))
                y += text.get_height() + Paragraph.line_spacing
                line = [word]
            else:
                line.append(word)
        if len(line) > 0:
            lines.append((y, Paragraph.render_line(line, font)))
        return lines

    @staticmethod
    def render_line(line, font):
        return font.render(' '.join(line), True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.get_image((self.w, self.h), *self.lines), self.position())

    @staticmethod
    @lru_cache()
    def get_image(size, *lines):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        for y, text in lines:
            surface.blit(text, (0, y))
        return surface


class CardDescription(ViewObject):
    margin = 6

    def __init__(self, app, card, board_width):
        w = CardImage.w * 3
        x = board_width - w if self.minion_in_left_lane(app, card) else 0
        self.card_type = card.type
        super().__init__(None, app, x, 0, w, CardImage.h * 3)
        header = Header(app, self.card_type.name, self.w / 2, self.margin * 3)
        children = [header]
        last_y = header.y + header.h + self.margin * 4

        for ability in self.card_type.abilities:
            children.append(Paragraph(
                app,
                paragraph=ability.description,
                x=self.margin * 3,
                y=last_y + self.margin * 6,
                max_w=self.w - self.margin * 6,
            ))
            last_y = children[-1].y + children[-1].h
        self.set_children(children)

    def minion_in_left_lane(self, app, card):
        return card.minion and card.minion.side.side_id in [side.side_id for side in app.board().lanes[0].sides]

    def draw(self, screen):
        screen.blit(self.get_image(self.w, self.h, self.margin), self.position())

    @staticmethod
    @lru_cache()
    def get_image(w, h, margin):
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, w, h), border_radius=margin)
        pygame.draw.rect(surface, CardImage.front_colour, (
            margin,
            margin,
            w - margin * 2,
            h - margin * 2,
        ))
        return surface
