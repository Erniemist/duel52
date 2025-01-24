import pygame


class Rotate:
    def __init__(self, rotation):
        self.rotation = rotation

    def apply(self, surface):
        pygame.transform.rotate(surface, self.rotation)
