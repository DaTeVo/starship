import pygame

from settings import (
    HEIGHT,
    PLAYER_MAX_BONUS_LIFE,
    PLAYER_RAPID_COOLDOWN,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SPEED,
    WIDTH,
)


def draw_ship(screen, x, y):
    points = [
        (x + 25, y),
        (x - 20, y - 15),
        (x - 10, y),
        (x - 20, y + 15),
    ]
    pygame.draw.polygon(screen, (220, 220, 255), points)
    pygame.draw.polygon(screen, (80, 160, 255), points, 2)

    flame = [
        (x - 20, y - 8),
        (x - 38, y),
        (x - 20, y + 8),
    ]
    pygame.draw.polygon(screen, (255, 120, 40), flame)


def damage_player(game):
    if game["bonus_life"] > 0:
        game["bonus_life"] -= 1
    else:
        game["player_life"] -= 1

    if game["player_life"] <= 0:
        game["game_over"] = True


def update_player(game, keys):
    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        game["ship_x"] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        game["ship_x"] += PLAYER_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_z]:
        game["ship_y"] -= PLAYER_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        game["ship_y"] += PLAYER_SPEED

    game["ship_x"] = max(30, min(WIDTH - 30, game["ship_x"]))
    game["ship_y"] = max(30, min(HEIGHT - 30, game["ship_y"]))

    for power_type in game["power_timers"]:
        if game["power_timers"][power_type] > 0:
            game["power_timers"][power_type] -= 1

    if game["shoot_cooldown"] > 0:
        game["shoot_cooldown"] -= 1

    rapid_is_active = game["power_timers"]["rapid"] > 0
    triple_is_active = game["power_timers"]["triple"] > 0
    laser_is_active = game["power_timers"]["laser"] > 0

    cooldown_time = PLAYER_RAPID_COOLDOWN if rapid_is_active else PLAYER_SHOOT_COOLDOWN
    bullet_type = "laser" if laser_is_active else "normal"

    if keys[pygame.K_SPACE] and game["shoot_cooldown"] == 0:
        if triple_is_active:
            game["bullets"].append([game["ship_x"] + 30, game["ship_y"] - 12, bullet_type])
            game["bullets"].append([game["ship_x"] + 30, game["ship_y"], bullet_type])
            game["bullets"].append([game["ship_x"] + 30, game["ship_y"] + 12, bullet_type])
        else:
            game["bullets"].append([game["ship_x"] + 30, game["ship_y"], bullet_type])

        game["shoot_cooldown"] = cooldown_time


def add_bonus_life(game):
    game["bonus_life"] = min(PLAYER_MAX_BONUS_LIFE, game["bonus_life"] + 1)
