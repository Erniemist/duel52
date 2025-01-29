import pygame

from App import App

FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode([1920, 1000])

    app = App(screen, "wss://duel52.herokuapp.com")
    while app.running:
        app.loop()

    pygame.quit()


if __name__ == '__main__':
    main()
