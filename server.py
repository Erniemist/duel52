import asyncio
import json

from websockets.asyncio.server import serve

from GameState import GameState
game = None


async def start(websocket):
    global game
    game = GameState()
    game.start_game()
    await websocket.send(json.dumps({'game': game.to_json(), 'team': 0}))


async def join(websocket):
    global game
    await websocket.send(json.dumps({'game': game.to_json(), 'team': 1}))


async def handler(websocket):
    global game
    async for message in websocket:
        data = json.loads(message)
        event = data['event']
        if event == 'init':
            if game is None:
                print('got init, starting game')
                await start(websocket)
            else:
                print('got init, joining game')
                await join(websocket)
        elif event == 'ping':
            await websocket.send(json.dumps(game.to_json()))
        else:
            print(event)
            game = GameState.from_json(data['game_state'])
            await websocket.send(json.dumps(data['game_state']))


async def main():
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
