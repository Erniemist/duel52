import asyncio
import json

import pygame
import websockets

from Cursor.Cursor import Cursor
from GameView import GameView
from GameState import GameState

LEFT = 1
RIGHT = 3


class App:
    def __init__(self, screen, websocket_uri):
        self.websocket_uri = websocket_uri
        self.screen = screen
        self.team = None
        self.game_state = None
        self.cursor = Cursor(self)
        self.last_focused = None
        self.game_view = None
        self.running = True
        self.tick = 0

    def send_message(self, message):
        return json.loads(asyncio.run(self.async_send_message(json.dumps(message))))

    async def async_send_message(self, message):
        async with websockets.connect(self.websocket_uri) as websocket:
            await websocket.send(message)
            return await websocket.recv()

    async def handle(self, message):
        response = json.loads(message)
        self.game_state = GameState.from_json(response['game'])
        if self.team is None:
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

    def loop(self):
        event_data = self.game_state.update()
        if not event_data:
            event_data = {'event': 'ping'}
        event_data['team'] = self.team

        game_data = self.send_message(event_data)
        self.game_state = GameState.from_json(game_data)

        self.cursor.position = pygame.mouse.get_pos()
        self.last_focused = self.game_view.focused_object if self.game_view else None
        self.game_view = GameView(self)
        self.handle_events()
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
