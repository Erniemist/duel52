from Server.CardTypes.Abilities.Backstab import Backstab
from Server.CardTypes.Abilities.Stealth import Stealth
from Server.CardTypes.CardType import CardType
from Server.CardTypes.Abilities.Two import Two
from Server.CardTypes.Abilities.Three import Three
from Server.CardTypes.Abilities.Four import Four
from Server.CardTypes.Abilities.Five import Five
from Server.CardTypes.Abilities.Six import Six
from Server.CardTypes.Abilities.Seven import Seven
from Server.CardTypes.Abilities.Eight import Eight
from Server.CardTypes.Abilities.Cleave import Cleave
from Server.CardTypes.Abilities.Jack import Jack
from Server.CardTypes.Abilities.Queen import Queen
from Server.CardTypes.Abilities.King import King
from Server.CardTypes.Abilities.Ace import Ace

types = {
    '2': lambda card: CardType(card, 'The Archivist', abilities=[Two]),
    '3': lambda card: CardType(card, 'Ambush!', abilities=[Three]),
    '4': lambda card: CardType(card, 'The Spy', abilities=[Four]),
    '5': lambda card: CardType(card, "The King's Banner", abilities=[Five]),
    '6': lambda card: CardType(card, 'The Frost Mage', abilities=[Six]),
    '7': lambda card: CardType(card, 'The Healer', abilities=[Seven]),
    '8': lambda card: CardType(card, 'The Thornbearer', abilities=[Eight]),
    '9': lambda card: CardType(card, 'The Ninja', abilities=[Stealth, Backstab]),
    '10': lambda card: CardType(card, 'The Berserker', abilities=[Cleave]),
    'J': lambda card: CardType(card, 'The Knight', abilities=[Jack], max_hp=3),
    'Q': lambda card: CardType(card, 'The Queen', abilities=[Queen]),
    'K': lambda card: CardType(card, 'The King', abilities=[King]),
    'A': lambda card: CardType(card, 'The Assassin', abilities=[Ace]),
}


def get_type(value):
    return types.get(value, lambda card: CardType(card))
