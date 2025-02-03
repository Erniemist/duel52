import pygame

from Client.ViewObject import ViewObject


class TargetView(ViewObject):
    weight = 5
    length = 20
    gap = 10

    def __init__(self, cursor, app, start, end):
        super().__init__(cursor, app, *start)
        self.start = start
        self.end = end

    def draw(self, screen: pygame.Surface):
        end_x, end_y = self.end
        start_x, start_y = self.start
        d_x, d_y = end_x - start_x, end_y - start_y
        distance = (d_x ** 2 + d_y ** 2) ** 0.5

        line_size = self.length + self.gap
        num_lines = int(distance // line_size)
        d_x, d_y = d_x / distance * line_size * num_lines, d_y / distance * line_size * num_lines
        if num_lines < 1:
            return

        line_d_x = d_x / num_lines
        line_d_y = d_y / num_lines
        line_starts = []
        line_ends = []
        for i in range(num_lines):
            time_modifier = i + self.app.tick % 100 / 100 + (1 - self.length / line_size)
            line_starts.append((
                start_x + line_d_x * min(max(1, time_modifier), num_lines),
                start_y + line_d_y * min(max(1, time_modifier), num_lines),
            ))
            line_ends.append((
                start_x + line_d_x * min(max(1, time_modifier + self.length / line_size), num_lines),
                start_y + line_d_y * min(max(1, time_modifier + self.length / line_size), num_lines),
            ))
        for start, end in zip(line_starts, line_ends):
            pygame.draw.line(screen, (255, 0, 0), start, end, self.weight)
