import math
import random

import pygame

from audio import play_sound
from settings import (
    BOSS_ATTACK_DELAY,
    BOSS_BOMB_EXPLOSION_AGE,
    BOSS_BOMB_FUSE,
    BOSS_BOMB_RADIUS,
    BOSS_BOMB_SPEED,
    BOSS_FRAGMENT_BOMB_FUSE,
    BOSS_LIFE_STEP,
    BOSS_SCORE_STEP,
    BOSS_SMALL_BOMB_RADIUS,
    BOSS_SPEED,
    BOSS_X,
    HEIGHT,
    WIDTH,
)


def boss_life_for_level(level):
    return BOSS_LIFE_STEP * (level + 1)


def create_boss(level):
    life = boss_life_for_level(level)

    return {
        "x": WIDTH + 90,
        "y": HEIGHT // 2,
        "life": life,
        "max_life": life,
        "direction": random.choice([-1, 1]),
        "attack_timer": BOSS_ATTACK_DELAY // 2,
        "level": level,
    }


def queue_boss(game):
    game["pending_bosses"].append(game["boss_level"])
    game["boss_level"] += 1
    game["next_boss_score"] += BOSS_SCORE_STEP
    game["enemy_spawn_count"] = min(
        game["max_enemy_spawn_count"],
        game["enemy_spawn_count"] + 1
    )


def spawn_pending_boss(game):
    if game["boss"] is None and len(game["pending_bosses"]) > 0:
        game["boss"] = create_boss(game["pending_bosses"].pop(0))


def handle_score_milestones(game):
    while game["score"] >= game["next_boss_score"]:
        queue_boss(game)

    spawn_pending_boss(game)


def update_boss(game):
    spawn_pending_boss(game)

    boss = game["boss"]

    if boss is not None:
        if boss["x"] > BOSS_X:
            boss["x"] -= BOSS_SPEED

        boss["y"] += boss["direction"] * BOSS_SPEED

        if boss["y"] < 70 or boss["y"] > HEIGHT - 70:
            boss["direction"] *= -1
            boss["y"] = max(70, min(HEIGHT - 70, boss["y"]))

        boss["attack_timer"] -= 1

        if boss["attack_timer"] <= 0:
            if random.random() < 0.35:
                spawn_fragment_bomb(game, boss)
            else:
                spawn_bomb(game, boss)

            boss["attack_timer"] = max(45, BOSS_ATTACK_DELAY - boss["level"] * 6)

    update_bombs(game)


def create_bomb(x, y, vx, vy, fuse, bomb_type, radius):
    return {
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "timer": fuse,
        "type": bomb_type,
        "radius": radius,
        "exploded": False,
        "age": 0,
        "has_damaged": False,
    }


def spawn_bomb(game, boss):
    game["boss_bombs"].append(create_bomb(
        boss["x"] - 50,
        boss["y"],
        -BOSS_BOMB_SPEED,
        0,
        BOSS_BOMB_FUSE,
        "normal",
        BOSS_BOMB_RADIUS,
    ))


def spawn_fragment_bomb(game, boss):
    game["boss_bombs"].append(create_bomb(
        boss["x"] - 50,
        boss["y"],
        -BOSS_BOMB_SPEED,
        0,
        BOSS_FRAGMENT_BOMB_FUSE,
        "fragment",
        BOSS_BOMB_RADIUS,
    ))


def spawn_small_bombs(game, bomb):
    speed = BOSS_BOMB_SPEED - 1
    directions = [(-speed, -speed), (-speed, speed), (speed, -speed), (speed, speed)]

    for vx, vy in directions:
        game["boss_bombs"].append(create_bomb(
            bomb["x"],
            bomb["y"],
            vx,
            vy,
            BOSS_FRAGMENT_BOMB_FUSE,
            "small",
            BOSS_SMALL_BOMB_RADIUS,
        ))


def update_bombs(game):
    for bomb in game["boss_bombs"][:]:
        if bomb["exploded"]:
            bomb["age"] += 1
            continue

        bomb["x"] += bomb["vx"]
        bomb["y"] += bomb["vy"]
        bomb["timer"] -= 1

        if bomb["y"] < 25 or bomb["y"] > HEIGHT - 25:
            bomb["vy"] *= -1
            bomb["y"] = max(25, min(HEIGHT - 25, bomb["y"]))

        if bomb["timer"] <= 0:
            explode_bomb(game, bomb)

    game["boss_bombs"] = [
        bomb for bomb in game["boss_bombs"]
        if -BOSS_BOMB_RADIUS < bomb["x"] < WIDTH + BOSS_BOMB_RADIUS
        and bomb["age"] <= BOSS_BOMB_EXPLOSION_AGE
    ]


def explode_bomb(game, bomb):
    if bomb["exploded"]:
        return

    bomb["exploded"] = True
    bomb["age"] = 0
    game["explosions"].append([bomb["x"], bomb["y"], 0])
    play_sound("explosion")

    if bomb["type"] == "fragment":
        spawn_small_bombs(game, bomb)


def boss_rect(boss):
    return pygame.Rect(boss["x"] - 55, boss["y"] - 42, 110, 84)


def bomb_rect(bomb):
    return pygame.Rect(bomb["x"] - 12, bomb["y"] - 12, 24, 24)


def player_is_in_bomb_radius(game, bomb):
    distance = math.hypot(game["ship_x"] - bomb["x"], game["ship_y"] - bomb["y"])
    return distance <= bomb["radius"]


def draw_boss(screen, boss, small_font):
    x = boss["x"]
    y = boss["y"]

    body = [
        (x - 55, y),
        (x - 20, y - 42),
        (x + 55, y - 30),
        (x + 35, y),
        (x + 55, y + 30),
        (x - 20, y + 42),
    ]
    pygame.draw.polygon(screen, (160, 60, 220), body)
    pygame.draw.polygon(screen, (245, 190, 255), body, 3)
    pygame.draw.circle(screen, (255, 90, 90), (int(x + 10), int(y)), 12)
    pygame.draw.circle(screen, (255, 220, 220), (int(x + 10), int(y)), 5)

    bar_width = 100
    life_ratio = boss["life"] / boss["max_life"]
    pygame.draw.rect(screen, (50, 20, 70), (x - 50, y - 62, bar_width, 8))
    pygame.draw.rect(screen, (255, 80, 120), (x - 50, y - 62, int(bar_width * life_ratio), 8))
    pygame.draw.rect(screen, (255, 220, 255), (x - 50, y - 62, bar_width, 8), 1)

    life_text = small_font.render(str(boss["life"]), True, (255, 255, 255))
    life_rect = life_text.get_rect(center=(x, y - 78))
    screen.blit(life_text, life_rect)


def draw_boss_bombs(screen, game):
    for bomb in game["boss_bombs"]:
        x = int(bomb["x"])
        y = int(bomb["y"])

        if bomb["exploded"]:
            radius = int(bomb["radius"] * (1 - bomb["age"] / BOSS_BOMB_EXPLOSION_AGE))
            pygame.draw.circle(screen, (255, 120, 40), (x, y), radius, 3)
            pygame.draw.circle(screen, (255, 220, 80), (x, y), max(4, radius // 3))
        elif bomb["type"] == "fragment":
            pygame.draw.circle(screen, (60, 180, 255), (x, y), 15)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 7)
        elif bomb["type"] == "small":
            pygame.draw.circle(screen, (255, 130, 60), (x, y), 8)
        else:
            pulse = 4 if bomb["timer"] % 20 < 10 else 0
            pygame.draw.circle(screen, (90, 40, 120), (x, y), 12 + pulse)
            pygame.draw.circle(screen, (255, 190, 70), (x, y), 8)
