import pygame.draw

import rectangle
from functions import can_call


class ViewObject:
    def __init__(self, real, game, x, y, w=0, h=0):
        self.real = real
        self.game = game
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

    def check_focus(self):
        for child in self.children[::-1]:
            child_focus = child.check_focus()
            if child_focus is not None:
                return child_focus
        return self.base_check_focus()

    def base_check_focus(self):
        cursor = self.game.cursor
        if not can_call(self.real, cursor.click_method_name()):
            return None
        if can_call(self.real, cursor.validation_method_name()) and not cursor.validation_method()(self.real):
            return None
        return self if self.touching_mouse() else None

    def rect(self):
        x, y = self.position()
        return x, y, self.w, self.h

    def touching_mouse(self):
        return rectangle.point_inside(self.game.cursor.position, self.rect())

    def draw_all(self, screen):
        self.draw(screen)
        for child in self.children:
            child.draw_all(screen)

    def position(self):
        if self.parent is None:
            return self._x, self._y
        x, y = self.parent.position()
        return self._x + x, self._y + y

    def call_recursive(self, method_name, callback):
        for child in self.children:
            child.call_recursive(method_name, callback)
        if can_call(self, method_name):
            callback(self)

    def draw(self, screen):
        pass
