class FaceDown:
    name = 'FaceDown'

    def could_choose(self, card):
        return card.minion is not None and card.minion.face_down
