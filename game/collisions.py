import pygame

from boss import (
    bomb_rect,
    boss_rect,
    explode_bomb,
    handle_score_milestones,
    player_is_in_bomb_radius,
)
from player import damage_player
from powerups import apply_powerup, spawn_powerup_drop
from settings import BOSS_CONTACT_COOLDOWN, BOSS_LASER_DAMAGE, BOSS_SCORE_REWARD


def bullet_rect(bullet):
    if bullet[2] == "laser":
        return pygame.Rect(bullet[0], bullet[1] - 6, 26, 12)

    return pygame.Rect(bullet[0], bullet[1] - 3, 12, 6)


def handle_collisions(game):
    if game["boss_contact_cooldown"] > 0:
        game["boss_contact_cooldown"] -= 1

    for bullet in game["bullets"][:]:
        current_bullet_rect = bullet_rect(bullet)

        for enemy in game["enemies"][:]:
            enemy_rect = pygame.Rect(enemy[0] - 25, enemy[1] - 15, 50, 30)

            if current_bullet_rect.colliderect(enemy_rect):
                game["enemies"].remove(enemy)
                game["explosions"].append([enemy[0], enemy[1], 0])
                game["score"] += 1
                handle_score_milestones(game)
                spawn_powerup_drop(game, enemy[0], enemy[1])

                if bullet[2] != "laser":
                    if bullet in game["bullets"]:
                        game["bullets"].remove(bullet)
                    break

        if bullet not in game["bullets"]:
            continue

        for bomb in game["boss_bombs"]:
            if not bomb["exploded"] and current_bullet_rect.colliderect(bomb_rect(bomb)):
                explode_bomb(game, bomb)

                if bullet[2] != "laser" and bullet in game["bullets"]:
                    game["bullets"].remove(bullet)
                break

        if bullet not in game["bullets"]:
            continue

        if game["boss"] is not None and current_bullet_rect.colliderect(boss_rect(game["boss"])):
            if bullet[2] == "laser":
                game["boss"]["life"] -= BOSS_LASER_DAMAGE
            else:
                game["boss"]["life"] -= 1

            if bullet in game["bullets"]:
                game["bullets"].remove(bullet)

            if game["boss"]["life"] <= 0:
                boss_x = game["boss"]["x"]
                boss_y = game["boss"]["y"]
                game["explosions"].append([boss_x, boss_y, 0])
                game["score"] += BOSS_SCORE_REWARD
                game["boss"] = None
                handle_score_milestones(game)

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

    if (
        game["boss"] is not None
        and game["boss_contact_cooldown"] == 0
        and player_rect.colliderect(boss_rect(game["boss"]))
    ):
        damage_player(game)
        game["boss_contact_cooldown"] = BOSS_CONTACT_COOLDOWN

    for bomb in game["boss_bombs"]:
        if not bomb["exploded"] and player_rect.colliderect(bomb_rect(bomb)):
            explode_bomb(game, bomb)

    for bomb in game["boss_bombs"]:
        if (
            bomb["exploded"]
            and not bomb["has_damaged"]
            and player_is_in_bomb_radius(game, bomb)
        ):
            damage_player(game)
            bomb["has_damaged"] = True

    for powerup in game["powerups"][:]:
        powerup_rect = pygame.Rect(powerup[0] - 15, powerup[1] - 15, 30, 30)

        if player_rect.colliderect(powerup_rect):
            game["powerups"].remove(powerup)
            apply_powerup(game, powerup[2])
