import pygame

from settings import (
    BULLET_SPEED,
    ENEMY_BULLET_SPEED,
    LASER_BULLET_SPEED_BONUS,
    WIDTH,
)


def update_projectiles(game):
    for bullet in game["bullets"]:
        if bullet[2] == "laser":
            bullet[0] += BULLET_SPEED + LASER_BULLET_SPEED_BONUS
        else:
            bullet[0] += BULLET_SPEED

    game["bullets"] = [
        bullet for bullet in game["bullets"]
        if bullet[0] < WIDTH + 40
    ]

    for enemy_bullet in game["enemy_bullets"]:
        enemy_bullet[0] -= ENEMY_BULLET_SPEED

    game["enemy_bullets"] = [
        enemy_bullet for enemy_bullet in game["enemy_bullets"]
        if enemy_bullet[0] > -20
    ]


def draw_projectiles(screen, game):
    for bullet in game["bullets"]:
        if bullet[2] == "laser":
            pygame.draw.rect(screen, (80, 220, 255), (bullet[0], bullet[1] - 6, 26, 12))
            pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1] - 2, 26, 4))
        else:
            pygame.draw.rect(screen, (255, 255, 80), (bullet[0], bullet[1] - 3, 12, 6))

    for enemy_bullet in game["enemy_bullets"]:
        pygame.draw.rect(screen, (255, 80, 80), (enemy_bullet[0], enemy_bullet[1] - 3, 12, 6))
