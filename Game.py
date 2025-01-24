import pygame

from Board.Board import Board
from Cursor.Cursor import Cursor
from Graveyard.Graveyard import Graveyard
from Player.Player import Player
from functions import can_call

LEFT = 1
RIGHT = 3


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.view_objects = []
        self.players = [Player(team, self) for team in Player.TEAMS]
        self.active_player = self.players[0]
        self.graveyard = Graveyard(self)
        self.board = Board(self)
        self.cursor = Cursor(self)
        self.displayables = [*self.players, self.board, self.cursor]
        self.focused_object = None
        self.running = True
        self.tick = 0

    def loop(self):
        self.cursor.position = pygame.mouse.get_pos()
        self.generate_view_objects()
        self.handle_events()
        self.screen.fill((64, 180, 64))
        for view_object in self.view_objects:
            view_object.draw_all(self.screen)
        self.tick += 1
        pygame.display.flip()

    def generate_view_objects(self):
        self.view_objects = []
        self.focused_object = None
        for displayable in self.displayables:
            view = displayable.view()
            if view:
                self.view_objects.append(view)

        self.focused_object = self.get_focused_object()

    def get_focused_object(self):
        for view_object in self.view_objects[::-1]:
            touched_object = view_object.check_focus(self, self.cursor.position)
            if touched_object is None:
                continue

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
            for view_object in self.view_objects:
                if can_call(view_object, 'on_mouse_move'):
                    view_object.on_mouse_move(self)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == RIGHT:
                self.cursor.cancel_target()
                return
            if event.button != LEFT:
                return
            if not self.focused_object:
                self.cursor.cancel_target()
                return
            self.cursor.click_method()(self.focused_object.real)
