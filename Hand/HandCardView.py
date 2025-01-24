from Card.CardView import CardView


class HandCardView(CardView):
    def __init__(self, card, hand, i, pos, rotation, facedown=False):
        self.hand = hand
        self.i = i
        super().__init__(card, pos, rotation, facedown)

    def on_focus(self):
        return self.hand.focus_card(self)
