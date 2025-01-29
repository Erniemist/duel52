import asyncio
import json
import os
import signal

from websockets.asyncio.server import serve

from Server.ServerGameState import ServerGameState
from Server.ServerPlayer import ServerPlayer

game = None


async def start(websocket):
    global game
    game = ServerGameState()
    team = ServerPlayer.TEAMS[0]
    await websocket.send(json.dumps({'game': game.to_json(team), 'team': team}))


async def join(websocket, game: ServerGameState):
    team = ServerPlayer.TEAMS[1]
    await websocket.send(json.dumps({'game': game.to_json(team), 'team': team}))


async def handle_event(websocket, data, game: ServerGameState):
    player = game.active_player()
    if player.team != data['team']:
        raise Exception(f'Non-active player attempted to take action: {data}')
    match data:
        case {'event': 'play', 'data': {'side': side, 'card': card}}:
            side = game.find_side(side)
            card = game.find_card_from_hand(card)
            player.play_card(card=card, side=side)

        case {'event': 'flip', 'data': {'card': card}}:
            minion = game.find_card_from_board(card).minion
            player.flip_minion(minion)

        case {'event': 'pair', 'data': {'card_1': card_1, 'card_2': card_2}}:
            minion_1 = game.find_card_from_board(card_1).minion
            minion_2 = game.find_card_from_board(card_2).minion
            player.pair_minions(minion_1, minion_2)

        case {'event': 'attack', 'data': {'card_1': card_1, 'card_2': card_2}}:
            minion_1 = game.find_card_from_board(card_1).minion
            minion_2 = game.find_card_from_board(card_2).minion
            player.attack(minion_1, minion_2)

        case _:
            raise Exception(f"Didn't recognise event: {data}")

    await websocket.send(json.dumps({'game': game.to_json(data['team'])}))


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
                await join(websocket, game)
        elif event == 'ping':
            await websocket.send(json.dumps({'game': game.to_json(data['team'])}))
        elif event == 'close':
            data = game.to_json(data['team'])
            game = None
            await websocket.send(json.dumps({'game': data}))
        else:
            await handle_event(websocket, data, game)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
