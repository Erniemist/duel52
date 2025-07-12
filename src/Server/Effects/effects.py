def discard(game, card):
    card.move_to(game.graveyard)


def draw(player):
    player.deck.draw_from_top(player.hand)
