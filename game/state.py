from settings import HEIGHT, WIDTH


def reset_game():
    return {
        "ship_x": WIDTH // 2,
        "ship_y": HEIGHT // 2,

        "player_life": 3,
        "bonus_life": 0,

        "bullets": [],
        "enemy_bullets": [],
        "enemies": [],
        "powerups": [],
        "explosions": [],

        "shoot_cooldown": 0,
        "spawn_timer": 0,
        "enemy_shoot_timer": 0,

        "score": 0,
        "game_over": False,

        "power_timers": {
            "triple": 0,
            "rapid": 0,
            "laser": 0,
        },
    }
