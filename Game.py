import pygame

from Cursor.Cursor import Cursor
from GameView import GameView
from Server.GameState import GameState

LEFT = 1
RIGHT = 3


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.game_state = GameState()
        self.cursor = Cursor(self)
        self.last_focused = None
        self.game_view = GameView(self)
        self.running = True
        self.tick = 0

    def players(self):
        return self.game_state.players

    def board(self):
        return self.game_state.board

    def active_player(self):
        return self.game_state.active_player()

    def loop(self):
        self.game_state.update()
        self.cursor.position = pygame.mouse.get_pos()
        self.last_focused = self.game_view.focused_object
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
