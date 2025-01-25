import pygame
import time

from Game import Game

FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)

    game = Game(screen)
    while game.running:
        game.loop()

    pygame.quit()


if __name__ == '__main__':
    main()
