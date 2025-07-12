from Client.Card.CardImage import CardImage
from Client.Card.CardView import CardView


class CursorCardView(CardView):
    shadow_scale = 1.1
    shadow_offset = (20, 20)
    perspective_scale = 1.1

    def __init__(self, card, app, pos):
        super().__init__(card, app, pos, CardImage.highlight)

    def image(self):
        return CardImage.make_image_with_shadow(
            self.style,
            False,
            self.card.value,
            self.w,
            self.h,
            self.shadow_offset,
            self.shadow_scale,
        )

    def on_mouse_move(self):
        self.card.x, self.card.y = self.app.cursor.position
