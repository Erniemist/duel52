import pygame
import time

from Game import Game

FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)

    game = Game(screen)
    prev_time = time.time()
    while game.running:
        game.loop()
        prev_time = fps_sleep(prev_time)

    pygame.quit()


def fps_sleep(prev_time):
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    sleep_time = 1. / FPS - dt
    if sleep_time > 0:
        time.sleep(sleep_time)
    return prev_time


if __name__ == '__main__':
    main()
