from Server.CardTypes.CardType import CardType
from Server.CardTypes.Abilities.Two import Two
from Server.CardTypes.Abilities.Three import Three
from Server.CardTypes.Abilities.Four import Four
from Server.CardTypes.Abilities.Five import Five
from Server.CardTypes.Abilities.Six import Six
from Server.CardTypes.Abilities.Seven import Seven
from Server.CardTypes.Abilities.Eight import Eight
from Server.CardTypes.Abilities.Ten import Ten
from Server.CardTypes.Abilities.Queen import Queen
from Server.CardTypes.Abilities.King import King
from Server.CardTypes.Abilities.Ace import Ace

types = {
    '2': lambda card: CardType(card, abilities=[Two]),
    '3': lambda card: CardType(card, abilities=[Three]),
    '4': lambda card: CardType(card, abilities=[Four]),
    '5': lambda card: CardType(card, abilities=[Five]),
    '6': lambda card: CardType(card, abilities=[Six]),
    '7': lambda card: CardType(card, abilities=[Seven]),
    '8': lambda card: CardType(card, abilities=[Eight]),
    '10': lambda card: CardType(card, abilities=[Ten]),
    'Q': lambda card: CardType(card, abilities=[Queen]),
    'K': lambda card: CardType(card, abilities=[King]),
    'A': lambda card: CardType(card, abilities=[Ace]),
}
