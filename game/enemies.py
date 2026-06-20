import random

import pygame

from settings import (
    ENEMY_SHOOT_DELAY,
    ENEMY_SPEED,
    ENEMY_SPAWN_DELAY,
    HEIGHT,
    WIDTH,
)


def draw_enemy(screen, x, y):
    points = [
        (x - 25, y),
        (x + 20, y - 15),
        (x + 10, y),
        (x + 20, y + 15),
    ]
    pygame.draw.polygon(screen, (255, 80, 80), points)
    pygame.draw.polygon(screen, (255, 180, 180), points, 2)


def update_enemies(game):
    game["spawn_timer"] += 1

    if game["spawn_timer"] >= ENEMY_SPAWN_DELAY:
        for index in range(game["enemy_spawn_count"]):
            game["enemies"].append([
                WIDTH + 40 + index * 45,
                random.randint(40, HEIGHT - 40),
            ])

        game["spawn_timer"] = 0

    game["enemy_shoot_timer"] += 1

    if game["enemy_shoot_timer"] >= ENEMY_SHOOT_DELAY and len(game["enemies"]) > 0:
        enemy = random.choice(game["enemies"])
        game["enemy_bullets"].append([enemy[0] - 30, enemy[1]])
        game["enemy_shoot_timer"] = 0

    for enemy in game["enemies"]:
        enemy[0] -= ENEMY_SPEED

    game["enemies"] = [
        enemy for enemy in game["enemies"]
        if enemy[0] > -50
    ]
