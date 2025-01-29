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
            await choose_game(websocket, await list_games(websocket))
            await app.start()
        await asyncio.gather(
            app.run(),
            app.handle_incoming()
        )


async def list_games(websocket):
    await websocket.send(json.dumps({'event': 'list'}))
    return json.loads(await websocket.recv())


async def choose_game(websocket, games):
    print('listing games')
    print('0) Create a new game')
    for i, game in enumerate(games):
        print(f'{i + 1}) {game.name}')
    choice = input('>>> ')
    try:
        choice = int(choice)
    except ValueError:
        return choose_game(websocket, games)
    if choice == 0:
        name = input('Enter game name: ')
        if name in [game.name for game in games]:
            return choose_game(websocket, games)
        websocket.send(json.dumps({'event': 'create', 'name': name}))
        return
    websocket.send(json.dumps({'event': 'join', 'game_id': games[choice - 1]['game_id']}))


if __name__ == '__main__':
    asyncio.run(main())
