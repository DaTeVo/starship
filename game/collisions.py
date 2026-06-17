import pygame

from player import damage_player
from powerups import apply_powerup, spawn_powerup_drop


def bullet_rect(bullet):
    if bullet[2] == "laser":
        return pygame.Rect(bullet[0], bullet[1] - 6, 26, 12)

    return pygame.Rect(bullet[0], bullet[1] - 3, 12, 6)


def handle_collisions(game):
    for bullet in game["bullets"][:]:
        current_bullet_rect = bullet_rect(bullet)

        for enemy in game["enemies"][:]:
            enemy_rect = pygame.Rect(enemy[0] - 25, enemy[1] - 15, 50, 30)

            if current_bullet_rect.colliderect(enemy_rect):
                game["enemies"].remove(enemy)
                game["explosions"].append([enemy[0], enemy[1], 0])
                game["score"] += 1
                spawn_powerup_drop(game, enemy[0], enemy[1])

                if bullet[2] != "laser":
                    if bullet in game["bullets"]:
                        game["bullets"].remove(bullet)
                    break

    player_rect = pygame.Rect(
        game["ship_x"] - 25,
        game["ship_y"] - 15,
        50,
        30
    )

    for enemy_bullet in game["enemy_bullets"][:]:
        enemy_bullet_rect = pygame.Rect(
            enemy_bullet[0],
            enemy_bullet[1] - 3,
            12,
            6
        )

        if enemy_bullet_rect.colliderect(player_rect):
            game["enemy_bullets"].remove(enemy_bullet)
            damage_player(game)

    for enemy in game["enemies"][:]:
        enemy_rect = pygame.Rect(enemy[0] - 25, enemy[1] - 15, 50, 30)

        if player_rect.colliderect(enemy_rect):
            game["enemies"].remove(enemy)
            game["explosions"].append([enemy[0], enemy[1], 0])
            damage_player(game)

    for powerup in game["powerups"][:]:
        powerup_rect = pygame.Rect(powerup[0] - 15, powerup[1] - 15, 30, 30)

        if player_rect.colliderect(powerup_rect):
            game["powerups"].remove(powerup)
            apply_powerup(game, powerup[2])
