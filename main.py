import asyncio
import json

import pygame

from App import App
from GameState import GameState

FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode([1920, 1000])

    app = App(screen, "ws://localhost:8001")
    response = app.send_message({'event': 'init'})
    app.game_state = GameState.from_json(response['game'])
    app.team = response['team']
    while app.running:
        app.loop()

    pygame.quit()


if __name__ == '__main__':
    main()
