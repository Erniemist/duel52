from Card.CardView import CardView


class HandCardView(CardView):
    def __init__(self, card, game, hand, i, pos, rotation, face_down=False):
        self.hand = hand
        self.i = i
        super().__init__(card, game, pos, rotation, face_down)
