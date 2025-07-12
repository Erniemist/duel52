from Client.CardChoice import CardChoice
from Client.Cursor.Target import Target


class ChoiceData:
    def __init__(self, card_ids, target_source_id, target_style, optional):
        self.card_ids = card_ids
        self.target_source_id = target_source_id
        self.target_style = target_style
        self.optional = optional

    @staticmethod
    def from_server(game, choice):
        return ChoiceData(
            [
                card.card_id
                for card in game.get_cards()
                if choice.could_choose(card)
            ],
            choice.target.source_id,
            choice.target.style,
            choice.optional,
        )

    def make_client(self, game):
        cards = [game.find_card(card_id) for card_id in self.card_ids]
        target = Target(self.target_source_id, self.target_style)
        return CardChoice(cards, target, self.optional)

    def to_json(self):
        return {
            'card_ids': self.card_ids,
            'target_source_id': self.target_source_id,
            'target_style': self.target_style,
            'optional': self.optional,
        }

    @staticmethod
    def from_json(data):
        return ChoiceData(
            data['card_ids'],
            data['target_source_id'],
            tuple(data['target_style']),
            data['optional'],
        )
