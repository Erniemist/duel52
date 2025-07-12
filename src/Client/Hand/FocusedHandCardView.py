from Client import rectangle
from Client.Card.CardImage import CardImage
from Client.Card.CardView import CardView


class FocusedHandCardView(CardView):
    zoom = 1.1

    def __init__(self, card, app, pos, face_down=False):
        super().__init__(
            card,
            app,
            pos,
            style=app.cursor.targetter.style if app.cursor.target_source() else CardImage.highlight,
            w=CardImage.w * self.zoom,
            h=CardImage.h * self.zoom,
        )
        self.face_down = face_down

    def image(self):
        return CardImage.make_image(self.style, self.face_down, self.card.value, self.w, self.h, rotation=0)

    def touching_mouse(self):
        return rectangle.point_inside(self.cursor.position, (*self.position(), self.w, self.h * 2))
