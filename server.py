import asyncio
import json
import os
import signal
import traceback

from websockets.asyncio.server import serve

from Server.ServerApp import ServerApp

apps = {}


async def list_games(websocket):
    await websocket.send(json.dumps([
        {
            'game_id': game_id,
            'name': app.name,
        }
        for game_id, app in apps.items()
        if len(app.teams) < 2
    ]))


async def handler(websocket):
    global apps
    try:
        async for message in websocket:
            try:
                match json.loads(message):
                    case {'event': 'list'}:
                        await list_games(websocket)
                    case {'event': 'create', 'name': name}:
                        app = ServerApp(name)
                        apps[app.game_id] = app
                        await app.create(websocket)
                    case {'event': 'join', 'game_id': game_id}:
                        await apps[game_id].join(websocket)
                    case {'event': 'close'}:
                        return
                    case data:
                        await websocket.app.handle_event(websocket, data)
            except Exception:
                print(traceback.format_exc())
    finally:
        if hasattr(websocket, 'app'):
            for connection in websocket.app.teams.keys():
                await connection.close()
            if websocket.app.game_id in apps.keys():
                apps.pop(websocket.app.game_id)
        else:
            await websocket.close()


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
