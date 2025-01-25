import pygame

from Cursor.Cursor import Cursor
from GameView import GameView
from Server.GameState import GameState
from functions import can_call

LEFT = 1
RIGHT = 3


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.game_state = GameState()
        self.cursor = Cursor(self)
        self.last_focused = None
        self.game_view = GameView(self)
        self.focused_object = None
        self.running = True
        self.tick = 0
        self.turns = 0

    def graveyard(self):
        return self.game_state.graveyard

    def players(self):
        return self.game_state.players

    def board(self):
        return self.game_state.board

    def active_player(self):
        return self.game_state.active_player()

    def loop(self):
        if self.active_player().actions == 0:
            self.game_state.new_turn()
        self.cursor.position = pygame.mouse.get_pos()
        self.last_focused = self.focused_object
        self.game_view = GameView(self)
        self.focused_object = self.get_focused_object()
        self.handle_events()
        self.screen.fill((64, 180, 64))
        self.game_view.draw_all(self.screen)
        self.tick += 1
        pygame.display.flip()

    def get_focused_object(self):
        touched_object = self.game_view.check_focus(self.cursor.position)
        if touched_object is None:
            return

        if can_call(touched_object, 'on_focus'):
            touched_object = touched_object.on_focus()
        touched_object.focused = True
        return touched_object

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
            if not self.focused_object:
                self.cursor.cancel_target()
                return
            self.cursor.click_method()(self.focused_object.real)
