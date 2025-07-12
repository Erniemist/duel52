import itertools

from Client.Actions.AttackAction import AttackAction
from Client.Actions.FlipAction import FlipAction
from Client.Actions.PairAction import PairAction
from Client.Actions.PlayAction import PlayAction
from Server.CardTypes.Abilities.Cleave import Cleave
from Server.CardTypes.Abilities.Jack import Jack


def proposals(player):
    yield from play_proposals(player)
    yield from flip_proposals(player)
    yield from attack_proposals(player)
    yield from pair_proposals(player)


def play_proposals(player):
    for card in player.hand.cards:
        for side in player.sides():
            yield PlayAction(card, side)

def flip_proposals(player):
    for minion in player.minions():
        if minion.face_down and not minion.frozen:
            yield FlipAction(minion)

def attack_proposals(player):
    for minion in player.minions():
        yield from attacks_for_minion(minion)

def attacks_for_minion(minion):
    if not minion.can_attack():
        return
    enemies = minion.side.other_side().minions()
    if any(enemy.has_active_keyword(Jack) for enemy in enemies):
        enemies = [enemy for enemy in enemies if enemy.has_active_keyword(Jack)]
    for enemy in enemies:
        yield AttackAction(minion, [enemy])
    if len(enemies) < 2 or not minion.has_active_keyword(Cleave):
        return
    for enemy1, enemy2 in itertools.combinations(enemies, 2):
        yield AttackAction(minion, [enemy1, enemy2])

def pair_proposals(player):
    pairable = [minion for minion in player.minions() if not minion.pair]
    for minion1, minion2 in itertools.permutations(pairable, 2):
        yield PairAction(minion1, minion2)

