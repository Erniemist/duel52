from functools import lru_cache

import pygame

from Client.ViewObject import ViewObject


class TargetView(ViewObject):
    weight = 5
    length = 20
    gap = 10

    def __init__(self, target_source, style, app, end):
        self.target_source = target_source
        self.style = style
        start = self.targetter_centre()
        super().__init__(target_source, app, *start)
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
        for i in range(num_lines):
            time_modifier = i + self.app.tick % 20 / 20 + (1 - self.length / line_size)
            start = (
                start_x + line_d_x * min(max(1, time_modifier), num_lines),
                start_y + line_d_y * min(max(1, time_modifier), num_lines),
            )
            end = (
                start_x + line_d_x * min(max(1, time_modifier + self.length / line_size), num_lines),
                start_y + line_d_y * min(max(1, time_modifier + self.length / line_size), num_lines),
            )
            diff = (end[0] - start[0] + line_size, end[1] - start[1] + line_size)
            surface = self.get_line_segment_image(diff, self.style, self.weight, line_size)
            draw_at = (start[0] - line_size, start[1] - line_size)
            screen.blit(surface, draw_at)

    @staticmethod
    @lru_cache(maxsize=20)
    def get_line_segment_image(diff, style, weight, line_size):
        surface = pygame.Surface((line_size * 2, line_size * 2), pygame.SRCALPHA)
        pygame.draw.line(surface, style, (line_size, line_size), diff, weight)
        return surface

    def targetter_centre(self):
        if self.target_source.pair:
            return self.target_source.view_object.parent.get_centre()
        return self.target_source.view_object.get_centre()
