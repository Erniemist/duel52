import pygame

from Client.Card.CardView import CardView
from Client.ViewObject import ViewObject


class Header(ViewObject):
    def __init__(self, app, text, x, y):
        font = pygame.font.SysFont('Arial', 40)
        self.text = font.render(text, True, (0, 0, 0))
        super().__init__(None, app, x, y, self.text.get_width(), self.text.get_height())

    def draw(self, screen):
        screen.blit(self.text, (self.x - self.w / 2, self.y))


class Paragraph(ViewObject):
    size = 24
    line_spacing = 2

    def __init__(self, app, paragraph, x, y, max_w):
        self.font = pygame.font.SysFont('Arial', 24)
        self.lines = self.wrap_text(paragraph, x, y, max_w)
        super().__init__(
            None,
            app,
            x,
            y,
            w=max(text.get_width() for x, y, text in self.lines),
            h=sum(text.get_height() for x, y, text in self.lines) + self.line_spacing * (len(self.lines) - 1),
        )

    def wrap_text(self, paragraph, x, y, max_w):
        lines = []
        words = paragraph.split(' ')
        line = []
        for word in words:
            potential_line = line + [word]
            potential_text = self.render_line(potential_line)
            if potential_text.get_width() >= max_w:
                text = self.render_line(line)
                lines.append((x, y, text))
                y += text.get_height() + self.line_spacing
                line = [word]
            else:
                line.append(word)
        if len(line) > 0:
            lines.append((x, y, self.render_line(line)))
        return lines

    def render_line(self, line):
        return self.font.render(' '.join(line), True, (0, 0, 0))

    def draw(self, screen):
        for x, y, text in self.lines:
            screen.blit(text, (x, y))


class CardDescription(ViewObject):
    margin = 6

    def __init__(self, app, card_type):
        self.card_type = card_type
        super().__init__(None, app, 0, 0, CardView.w * 3, CardView.h * 3)
        header = Header(app, self.card_type.name, self.x + self.w / 2, self.y + self.margin * 3)
        children = [header]
        last_y = header.y + header.h + self.margin * 4

        for ability in self.card_type.abilities:
            children.append(Paragraph(
                app,
                paragraph=ability.description,
                x=self.margin * 3,
                y=last_y + self.margin,
                max_w=self.w - self.margin * 6,
            ))
            last_y = children[-1].y + children[-1].h
        self.set_children(children)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), border_radius=self.margin)
        pygame.draw.rect(screen, CardView.front_colour, (
            self.x + self.margin,
            self.y + self.margin,
            self.w - self.margin * 2,
            self.h - self.margin * 2,
        ))
