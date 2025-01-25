from Card.CardView import CardView


class HandCardView(CardView):
    def __init__(self, card, hand, i, pos, rotation, face_down=False):
        self.hand = hand
        self.i = i
        super().__init__(card, pos, rotation, face_down)
