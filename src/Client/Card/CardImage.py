from functools import lru_cache

import pygame


class CardImage:
    w = 125
    h = 175
    weight = 4
    font_size = 30
    back_colour = (230, 100, 100)
    back_colour_frozen = (200, 70, 125)
    front_colour = (230, 230, 230)
    front_colour_frozen = (200, 200, 255)
    highlight = (255, 255, 0)
    normal = (0, 0, 0)

    @staticmethod
    @lru_cache()
    def make_image(style, face_down, value, w, h, rotation):
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        card = CardImage.draw_card(style, face_down, value, w, h, surface)
        return pygame.transform.rotate(card, rotation)

    @staticmethod
    @lru_cache()
    def make_image_with_shadow(style, face_down, value, w, h, shadow_offset, shadow_scale):
        shadow_x, shadow_y = shadow_offset
        shadow_w, shadow_h = w * shadow_scale, h * shadow_scale
        surface = pygame.Surface((shadow_x + shadow_w, shadow_y + shadow_h), pygame.SRCALPHA)
        pygame.draw.rect(
            surface,
            (0, 0, 0, 80),
            (shadow_x, shadow_y, shadow_w, shadow_h),
            border_radius=CardImage.weight,
        )
        return CardImage.draw_card(style, face_down, value, w, h, surface)

    @staticmethod
    @lru_cache()
    def draw_card(style, face_down, value, w, h, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            style,
            (0, 0, w, h),
            border_radius=CardImage.weight
        )

        if face_down:
            pygame.draw.rect(
                screen,
                CardImage.back_colour,
                (CardImage.weight, CardImage.weight, w - CardImage.weight * 2, h - CardImage.weight * 2),
                border_radius=CardImage.weight
            )
            return screen
        pygame.draw.rect(
            screen,
            CardImage.front_colour,
            (CardImage.weight, CardImage.weight, w - CardImage.weight * 2, h - CardImage.weight * 2),
            border_radius=CardImage.weight
        )
        font = pygame.font.SysFont('arial', CardImage.font_size)
        numeral = font.render(value, True, (0, 0, 0))

        screen.blit(numeral, (
            w / 2 - numeral.get_width() / 2,
            h / 2 - numeral.get_height() / 2,
        ))
        return screen
