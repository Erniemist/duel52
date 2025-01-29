import asyncio

import pygame
import websockets

from App import App

FPS = 30

app = None


async def main():
    global app
    async with websockets.connect("wss://duel52-8b7c8276f3dd.herokuapp.com") as websocket:
        if app is None:
            pygame.init()
            screen = pygame.display.set_mode([1920, 1000])
            app = App(screen, websocket)
            await app.start()
        await asyncio.gather(
            app.run(),
            app.handle_incoming()
        )


if __name__ == '__main__':
    asyncio.run(main())
