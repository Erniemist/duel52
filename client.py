import asyncio
import json

import pygame
import websockets

from App import App

app = None
URI = "wss://duel52-8b7c8276f3dd.herokuapp.com"


async def main():
    global app
    async with websockets.connect(URI) as websocket:
        if app is None:
            pygame.init()
            screen = pygame.display.set_mode([1920, 1000])
            app = App(screen, websocket)
            await app.start()
        await asyncio.gather(
            app.run(),
            app.handle_incoming()
        )


async def list_games():
    async with websockets.connect(URI) as websocket:
        await websocket.send(json.dumps({'event': 'list'}))
        return await websocket.recv()


if __name__ == '__main__':
    games = asyncio.run(list_games())
    for game in games:
        print(game)
    exit()
    asyncio.run(main())
