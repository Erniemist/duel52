import asyncio
import json
from dotenv import dotenv_values
import pygame
import websockets

from App import App

URI = dotenv_values(".env.local").get('WEBSOCKET_URI')
URI = "wss://duel52-8b7c8276f3dd.herokuapp.com" if not URI else URI

app = None


async def main():
    global app
    async with websockets.connect(URI) as websocket:
        if app is None:
            await choose_game(websocket, await list_games(websocket))
            pygame.init()
            screen = pygame.display.set_mode([1920, 1000])
            app = App(screen, websocket)
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
        print(f'{i + 1}) {game['name']}')
    choice = input('>>> ')
    try:
        choice = int(choice)
        if choice > len(games):
            return await choose_game(websocket, games)
    except ValueError:
        return await choose_game(websocket, games)
    if choice == 0:
        name = input('Enter game name: ')
        if name in [game.name for game in games]:
            return await choose_game(websocket, games)
        await websocket.send(json.dumps({'event': 'create', 'name': name}))
        return
    await websocket.send(json.dumps({'event': 'join', 'game_id': games[choice - 1]['game_id']}))


if __name__ == '__main__':
    asyncio.run(main())
