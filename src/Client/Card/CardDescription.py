import pygame

from Client.Card.CardView import CardView
from Client.ViewObject import ViewObject


class CardDescription(ViewObject):
    margin = 6

    def __init__(self, app, card):
        self.card = card
        super().__init__(None, app, 0, 0, CardView.w * 3, CardView.h * 3)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, CardView.front_colour, (
            self.x + self.margin,
            self.y + self.margin,
            self.w - self.margin * 2,
            self.h - self.margin * 2,
        ))
        font = pygame.font.SysFont('Arial', 40)
        card_name = font.render(self.card.type.name, True, (0, 0, 0))
        screen.blit(card_name, (
                self.w / 2 - card_name.get_width() / 2,
                self.margin * 3,
        ))
        font = pygame.font.SysFont('Arial', 24)
        for ability in self.card.type.abilities:
            ability_text = font.render(ability.description, True, (0, 0, 0))
            screen.blit(ability_text, (
                self.margin * 3,
                self.margin * 5 + card_name.get_height(),
            ))
