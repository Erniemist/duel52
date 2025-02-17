from Client import rectangle
from Client.Card.CardView import CardView


class FocusedHandCardView(CardView):
    zoom = 1.1

    def __init__(self, card, app, pos, face_down=False):
        super().__init__(
            card,
            app,
            pos,
            face_down=face_down,
            w=CardView.w * self.zoom,
            h=CardView.h * self.zoom,
            style=app.cursor.targetter.style if app.cursor.target_source() else self.highlight,
        )

    def touching_mouse(self):
        return rectangle.point_inside(self.cursor.position, (*self.position(), self.w, self.h * 2))
