import asyncio
import json
import os
import signal

from websockets.asyncio.server import serve

from Server.ServerGameState import ServerGameState
from Server.ServerPlayer import ServerPlayer
from ServerApp import ServerApp

apps = {}


async def create(websocket, name):
    global apps
    app = ServerApp(ServerGameState(), name)
    apps[app.game_id] = app
    team = ServerPlayer.TEAMS[0]
    app.add_connection(websocket, team)
    await websocket.send(json.dumps({'game': app.to_json(websocket), 'team': team}))


async def join(websocket, game_id):
    team = ServerPlayer.TEAMS[1]
    app = apps[game_id]
    app.add_connection(websocket, team)
    await websocket.send(json.dumps({'game': app.to_json(websocket), 'team': team}))


async def handle_event(websocket, data):
    app = websocket.app
    player = app.game.active_player()
    if player.team != app.teams[websocket]:
        raise Exception(f'Non-active player attempted to take action: {data}')
    match data:
        case {'event': 'play', 'data': {'side': side, 'card': card}}:
            side = app.game.find_side(side)
            card = app.game.find_card_from_hand(card)
            player.play_card(card=card, side=side)

        case {'event': 'flip', 'data': {'card': card}}:
            minion = app.game.find_card_from_board(card).minion
            player.flip_minion(minion)

        case {'event': 'pair', 'data': {'card_1': card_1, 'card_2': card_2}}:
            minion_1 = app.game.find_card_from_board(card_1).minion
            minion_2 = app.game.find_card_from_board(card_2).minion
            player.pair_minions(minion_1, minion_2)

        case {'event': 'attack', 'data': {'card_1': card_1, 'card_2': card_2}}:
            minion_1 = app.game.find_card_from_board(card_1).minion
            minion_2 = app.game.find_card_from_board(card_2).minion
            player.attack(minion_1, minion_2)

        case _:
            raise Exception(f"Didn't recognise event: {data}")

    await websocket.send(json.dumps({'game': app.to_json(websocket)}))


async def handler(websocket):
    global apps
    try:
        async for message in websocket:
            match json.loads(message):
                case {'event': 'list'}:
                    await list_games(websocket)
                case {'event': 'create', 'name': name}:
                    await create(websocket, name)
                case {'event': 'join', 'game_id': game_id}:
                    await join(websocket, game_id)
                case {'event': 'ping'}:
                    await websocket.send(json.dumps({'game': websocket.app.to_json(websocket)}))
                case {'event': 'close'}:
                    apps.pop(websocket.app.game_id)
                case data:
                    await handle_event(websocket, data)
    finally:
        apps.pop(websocket.app.game_id)


async def list_games(websocket):
    await websocket.send(json.dumps([
        {
            'game_id': app.game_id,
            'name': app.name,
        }
        for app in apps
        if len(app.teams) < 2
    ]))


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
