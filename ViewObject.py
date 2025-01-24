import pygame.draw

import rectangle
from functions import can_call


class ViewObject:
    def __init__(self, real, x, y, w=0, h=0):
        self.real = real
        self.parent = None
        self._x = x
        self._y = y
        self.w = w
        self.h = h
        self.children = []
        self.focused = False

    def set_children(self, children):
        self.children = children
        for child in self.children:
            child.parent = self

    def check_focus(self, game, mouse):
        for child in self.children[::-1]:
            child_focus = child.check_focus(game, mouse)
            if child_focus is not None:
                return child_focus
        return self.base_check_focus(game, mouse)

    def base_check_focus(self, game, mouse):
        if not can_call(self.real, game.cursor.click_method_name()):
            return None
        if can_call(self.real, game.cursor.validation_method_name()) and not game.cursor.validation_method()(self.real):
            return None
        return self if self.touching_mouse(mouse) else None

    def rect(self):
        x, y = self.position()
        return x, y, self.w, self.h

    def touching_mouse(self, mouse):
        return rectangle.point_inside(mouse, self.rect())

    def draw_all(self, screen):
        self.draw(screen)
        for child in self.children:
            child.draw_all(screen)

    def position(self):
        if self.parent is None:
            return self._x, self._y
        x, y = self.parent.position()
        return self._x + x, self._y + y

    def draw(self, screen):
        pass
