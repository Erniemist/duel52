import math

import pygame

from Client.Board.Lane.Side.Minion.MinionView import MinionView
from Client.Board.Lane.Side.Pair.PairView import PairView
from Client.ViewObject import ViewObject


class SideView(ViewObject):
    margin = 10
    weight = 6

    def __init__(self, side, app, x, y, w, h):
        super().__init__(side, app, x + 1, y, w, h)
        self.side = self.real
        self.minion_views = self.generate_minion_views()
        self.set_children(self.minion_views)

    def draw(self, screen):
        if self.focused:
            pygame.draw.rect(screen, (255, 255, 0), (*self.position(), self.w, self.h), 6)

    def generate_minion_views(self):
        row_max = 4
        pairs = []
        minions = []
        for card in self.side.cards:
            if card.minion.pair:
                if card.minion.pair not in pairs:
                    pairs.append(card.minion)
            else:
                minions.append(card.minion)
        num_minions = len(minions) + len(pairs)
        num_rows = math.ceil(num_minions / row_max)

        return [
            (
                MinionView(minion, self.app, self.minion_position(i, num_minions, num_rows))
                if not minion.pair
                else PairView(minion, minion.pair, self.app, self.minion_position(i, num_minions, num_rows))
            )
            for i, minion in enumerate(minions + pairs)
        ]

    def minion_position(self, i, num_minions, num_rows):
        minions_per_row = math.ceil(num_minions / num_rows)
        row = i // minions_per_row
        col = i % minions_per_row
        minions_in_row = minions_per_row if row < (num_rows - 1) else (num_minions - row * minions_per_row)
        row_width = MinionView.w * minions_in_row + self.margin * (minions_in_row - 1)
        total_height = MinionView.h * num_rows + self.margin * (num_rows - 1)
        x_start = self.w / 2 - row_width / 2
        y_start = self.h / 2 - total_height / 2
        return (
            x_start + col * (MinionView.w + self.margin),
            y_start + row * (MinionView.h + self.margin),
        )
