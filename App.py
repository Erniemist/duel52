import asyncio
import json

import pygame
import websockets

from ClientGameState import ClientGameState
from Cursor.Cursor import Cursor
from GameView import GameView

LEFT = 1
RIGHT = 3


class App:
    def __init__(self, screen, websocket):
        self.websocket = websocket
        self.screen = screen
        self.team = None
        self.game_state = None
        self.cursor = Cursor(self)
        self.last_focused = None
        self.game_view = None
        self.running = True
        self.tick = 0

    async def start(self):
        await self.update({'event': 'init'})

    async def update(self, event_data):
        if self.team:
            event_data['team'] = self.team
        await self.websocket.send(json.dumps(event_data))

    async def handle_incoming(self):
        async for message in self.websocket:
            response = json.loads(message)
            self.game_state = ClientGameState.from_json(response['game'])
            if not self.team:
                self.team = response['team']

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
        event_data = self.game_state.update()
        if event_data:
            await self.update(event_data)
        elif self.tick % 30 == 0 and self.team is not self.active_player().team:
            event_data = {'event': 'ping'}
            await self.update(event_data)

        self.cursor.position = pygame.mouse.get_pos()
        self.last_focused = self.game_view.focused_object if self.game_view else None
        self.game_view = GameView(self)
        self.handle_events()
        self.game_view = GameView(self)
        self.game_view.draw_all(self.screen)
        pygame.display.flip()
        self.tick += 1

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
        await self.update({'event': 'close'})
