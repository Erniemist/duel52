import asyncio
import json
import os
import signal
import traceback

from websockets.asyncio.server import serve, ServerConnection

from Server.ServerApp import ServerApp
from Server.ServerGameState import ServerGameState

apps: dict[ServerConnection, ServerApp] = {}


async def list_games(websocket: ServerConnection):
    await websocket.send(json.dumps([
        {
            'game_id': app.game_id,
            'name': app.name,
        }
        for app in apps.values()
        if len(app.teams) < 2
    ]))


async def handler(websocket: ServerConnection):
    global apps
    try:
        async for message in websocket:
            try:
                match json.loads(message):
                    case {'action': 'list'}:
                        await list_games(websocket)
                    case {'action': 'create', 'name': name}:
                        app = ServerApp(name, ServerGameState())
                        apps[websocket] = app
                        await app.create(websocket)
                    case {'action': 'join', 'game_id': game_id}:
                        app = next(app for app in apps.values() if app.game_id == game_id)
                        apps[websocket] = app
                        await app.join(websocket)
                    case {'action': 'close'}:
                        return
                    case data:
                        await apps[websocket].handle_action(websocket, data)
            except Exception:
                print(traceback.format_exc())
    finally:
        if websocket in apps.keys():
            for connection in apps[websocket].teams.keys():
                await connection.close()
                apps.pop(websocket)
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
