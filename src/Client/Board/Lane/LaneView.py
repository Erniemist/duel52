import pygame

from Client.Board.Lane.Side.SideView import SideView
from Client.ViewObject import ViewObject


class LaneView(ViewObject):
    weight = 6

    def __init__(self, lane, app, x, y, w, h):
        super().__init__(lane, app, x + self.weight / 2, y, w - self.weight, h)
        self.lane = self.real
        self.side_views = self.generate_side_views()
        self.set_children(self.side_views)

    def generate_side_views(self):
        side_h = self.h / 2
        return [SideView(
            side,
            self.app,
            0,
            side_h * (1 if side.team == self.app.team else 0),
            self.w,
            side_h,
        ) for side in self.lane.sides]

    def draw(self, screen):
        x, y = self.position()
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (x - self.weight / 2, y),
            (x - self.weight / 2, y + self.h),
            self.weight,
        )
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (x + self.w + self.weight / 2, y),
            (x + self.w + self.weight / 2, y + self.h),
            self.weight,
        )
