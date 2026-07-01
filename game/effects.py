import math

import pygame

from settings import EXPLOSION_MAX_AGE


def draw_explosion(screen, x, y, age, max_age):
    progress = age / max_age
    radius = int(8 + progress * 32)

    pygame.draw.circle(screen, (255, 180, 40), (x, y), radius, 2)
    pygame.draw.circle(screen, (255, 80, 30), (x, y), max(2, radius // 2), 1)

    for angle in range(0, 360, 45):
        rad = math.radians(angle)

        start_x = x + int(math.cos(rad) * radius * 0.4)
        start_y = y + int(math.sin(rad) * radius * 0.4)

        end_x = x + int(math.cos(rad) * radius)
        end_y = y + int(math.sin(rad) * radius)

        pygame.draw.line(screen, (255, 220, 80), (start_x, start_y), (end_x, end_y), 2)


def update_explosions(game):
    for explosion in game["explosions"]:
        explosion[2] += 1

    game["explosions"] = [
        explosion
        for explosion in game["explosions"]
        if explosion[2] <= EXPLOSION_MAX_AGE
    ]
