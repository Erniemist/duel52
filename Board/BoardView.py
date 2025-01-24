import math

from Board.Lane.LaneView import LaneView
from ViewObject import ViewObject


class BoardView(ViewObject):
    def __init__(self, board, w, h):
        super().__init__(board, 0, 0, w, h)
        lane_w = int(math.ceil((self.w + LaneView.weight) / 3))
        lane_h = self.h * 0.65
        self.board = self.real
        self.lane_views = [
            LaneView(
                lane,
                i * lane_w - LaneView.weight / 2,
                (self.h - lane_h) / 2,
                lane_w,
                lane_h,
            )
            for i, lane in enumerate(self.board.lanes)
        ]
        self.set_children(self.lane_views)
