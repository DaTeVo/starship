import random

import pygame

from settings import PLAYER_MAX_LIFE, POWERUP_DURATION, POWERUP_SPEED
from player import add_bonus_life


POWERUP_COLORS = {
    "triple": (180, 100, 255),
    "rapid": (100, 255, 120),
    "laser": (80, 220, 255),
    "heal1": (80, 255, 120),
    "heal2": (40, 220, 80),
    "bonus_heart": (255, 220, 40),
}

POWERUP_LETTERS = {
    "triple": "T",
    "rapid": "R",
    "laser": "L",
    "heal1": "+1",
    "heal2": "+2",
    "bonus_heart": "♥",
}


def draw_powerup(screen, x, y, power_type, font):
    color = POWERUP_COLORS[power_type]
    letter = POWERUP_LETTERS[power_type]

    pygame.draw.circle(screen, color, (x, y), 15)
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 15, 2)

    text = font.render(letter, True, (10, 10, 20))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def update_powerups(game):
    for powerup in game["powerups"]:
        powerup[0] -= POWERUP_SPEED

    game["powerups"] = [powerup for powerup in game["powerups"] if powerup[0] > -30]


def spawn_powerup_drop(game, x, y):
    drop_chance = random.random()

    if drop_chance < 0.25:
        power_type = random.choice(["triple", "rapid", "laser"])
        game["powerups"].append([x, y, power_type])
    elif drop_chance < 0.35:
        game["powerups"].append([x, y, "heal1"])
    elif drop_chance < 0.39:
        game["powerups"].append([x, y, "heal2"])
    elif drop_chance < 0.44:
        game["powerups"].append([x, y, "bonus_heart"])


def apply_powerup(game, power_type):
    if power_type == "heal1":
        game["player_life"] = min(PLAYER_MAX_LIFE, game["player_life"] + 1)
    elif power_type == "heal2":
        game["player_life"] = min(PLAYER_MAX_LIFE, game["player_life"] + 2)
    elif power_type == "bonus_heart":
        add_bonus_life(game)
    else:
        game["power_timers"][power_type] = POWERUP_DURATION
