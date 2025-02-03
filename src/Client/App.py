import asyncio
import json
import traceback

import pygame

from Client.ClientGameState import ClientGameState
from Client.Cursor.Cursor import Cursor
from DataTransfer.GameData import GameData
from Client.GameView import GameView
from Server.ServerApp import ServerApp

LEFT = 1
RIGHT = 3


class App:
    def __init__(self, screen, websocket):
        self.websocket = websocket
        self.screen = screen
        self.team = None
        self.game_state: None | ClientGameState = None
        self.cursor = Cursor(self)
        self.game_view = None
        self.running = True
        self.events = []
        self.tick = 0
        self.fake_server: None | ServerApp = None

    async def update(self, event):
        event.sent = True
        try:
            self.fake_server.resolve_action(event.json())
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        self.game_state = GameData.from_server(self.fake_server.game, self.team).make_client(self)
        await self.websocket.send(json.dumps(event.json()))

    async def handle_incoming(self):
        async for message in self.websocket:
            response = json.loads(message)
            if 'event_id' in response.keys():
                self.game_state.resolve(response['event_id'])
            game_data = GameData.from_json(response['game'])
            self.game_state = game_data.make_client()
            if not self.team:
                self.team = response['team']
            self.fake_server = ServerApp(name='fake', game=game_data.make_server())

    def players(self):
        return self.game_state.players

    def board(self):
        return self.game_state.board

    def active_player(self):
        return self.game_state.active_player()

    def is_my_turn(self):
        return self.game_state.active_player().team == self.team

    def find_card_from_hand(self, card_id):
        return self.game_state.find_card_from_hand(card_id)

    def find_card_from_board(self, card_id):
        return self.game_state.find_card_from_board(card_id)

    async def run(self):
        try:
            while self.running:
                if self.game_state:
                    await self.loop()
                await asyncio.sleep(0)
        finally:
            await self.close()
            pygame.quit()

    async def loop(self):
        event = self.game_state.next_event()
        if event and not event.sent:
            await self.update(event)
        self.cursor.position = pygame.mouse.get_pos()
        self.game_view = GameView(self)
        self.handle_events()
        self.game_view = GameView(self)
        self.game_view.draw_all(self.screen)
        pygame.display.flip()
        self.tick += 1

    def focused_object(self):
        if self.game_view is None:
            return None
        return self.game_view.focused_object

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.MOUSEMOTION:
            self.game_view.call_recursive('on_mouse_move', lambda x: x.on_mouse_move())
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == RIGHT:
                self.cursor.cancel()
                return
            if event.button != LEFT:
                return
            if not self.game_view.focused_object:
                self.cursor.cancel_target()
                return
            self.cursor.click_method()(self.game_view.focused_object.real)

    async def close(self):
        self.running = False
        await self.websocket.send(json.dumps({'event': 'close'}))
        await self.websocket.close()
