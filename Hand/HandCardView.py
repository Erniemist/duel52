from Card.CardView import CardView


class HandCardView(CardView):
    def __init__(self, card, app, hand, i, pos, rotation, face_down=False):
        self.hand = hand
        self.i = i
        super().__init__(card, app, pos, rotation, face_down)
