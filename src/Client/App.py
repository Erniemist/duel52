import asyncio
import json
import traceback

import pygame

from Client.Board.Lane.Side.Minion.MinionView import MinionView
from Client.ClientGameState import ClientGameState
from Client.Cursor.Cursor import Cursor
from Client.Cursor.Target import Target
from DataTransfer.ChoiceData import ChoiceData
from DataTransfer.GameData import GameData
from Client.GameView import GameView
from Server.Choices.CardChoice import CardChoice
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
        self.actions = []
        self.tick = 0
        self.clock = pygame.time.Clock()
        self.fake_server: None | ServerApp = None
        self.awaiting_choice: None | CardChoice = None

    async def update(self, action):
        action.sent = True
        try:
            self.fake_server.resolve_action(action.json(), self.team)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        await self.websocket.send(json.dumps(action.json()))

    async def handle_incoming(self):
        async for message in self.websocket:
            response = json.loads(message)
            if 'action_id' in response.keys():
                self.mark_action_as_resolved(response['action_id'])
            game_data = GameData.from_json(response['game'])
            self.game_state = game_data.make_client()
            self.fake_server = ServerApp(name='fake', game=game_data.make_server())
            if 'awaiting_choice' in response.keys():
                self.set_awaiting_choice(response)
                self.fake_server.game.awaited_choices.append(
                    CardChoice([], self.game_state, self.my_player())
                )
            if not self.team:
                self.team = response['team']

    def set_awaiting_choice(self, response):
        self.awaiting_choice = ChoiceData.from_json(response['awaiting_choice']).make_client(self.game_state)
        self.cursor.set_target_source(self.awaiting_choice.target)

    def players(self):
        return self.game_state.players

    def board(self):
        return self.game_state.board

    def active_player(self):
        return self.game_state.active_player()

    def my_player(self):
        return next(player for player in self.players() if player.team == self.team)

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
        self.actions += self.game_state.actions
        action = self.next_action()
        if action and not action.sent:
            await self.update(action)
            self.game_state = GameData.from_server(self.fake_server.game, self.team).make_client()
        self.cursor.position = pygame.mouse.get_pos()
        self.game_view = GameView(self)
        self.set_target_style()
        self.game_view = GameView(self)
        self.game_view.draw_all(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
        self.tick += 1

    def set_target_style(self):
        if not self.cursor.target_source() or self.awaiting_choice:
            return
        if not self.focused_object() or not isinstance(self.focused_object(), MinionView):
            self.cursor.set_target_source(Target.harm(self.cursor.target_source()))
            return
        if self.focused_object().minion.side.side_id != self.cursor.target_source().side.side_id:
            self.cursor.set_target_source(Target.harm(self.cursor.target_source()))
            return
        self.cursor.set_target_source(Target.affect(self.cursor.target_source()))

    def next_action(self):
        return next((action for action in self.actions if not action.resolved), None)

    def mark_action_as_resolved(self, action_id):
        action = next(action for action in self.actions if action.action_id == action_id)
        action.resolved = True
        if action.name == 'choose':
            self.awaiting_choice = None

    def focused_object(self):
        if self.game_view is None:
            return None
        return self.game_view.focused_object

    async def user_input(self):
        while self.running:
            if self.game_view:
                self.handle_events()
            await asyncio.sleep(0)

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
                self.cursor.cancel()
                return
            self.cursor.click_method()(self.game_view.focused_object.real)

    async def close(self):
        self.running = False
        await self.websocket.send(json.dumps({'action': 'close'}))
        await self.websocket.close()
