from settings import BOSS_SCORE_STEP, ENEMY_MAX_SPAWN_COUNT, HEIGHT, WIDTH


def reset_game():
    return {
        "ship_x": WIDTH // 2,
        "ship_y": HEIGHT // 2,

        "player_life": 3,
        "bonus_life": 0,

        "bullets": [],
        "enemy_bullets": [],
        "boss_bombs": [],
        "enemies": [],
        "boss": None,
        "pending_bosses": [],
        "powerups": [],
        "explosions": [],

        "shoot_cooldown": 0,
        "spawn_timer": 0,
        "enemy_shoot_timer": 0,
        "boss_contact_cooldown": 0,

        "score": 0,
        "next_boss_score": BOSS_SCORE_STEP,
        "boss_level": 0,
        "enemy_spawn_count": 1,
        "max_enemy_spawn_count": ENEMY_MAX_SPAWN_COUNT,
        "game_over": False,

        "power_timers": {
            "triple": 0,
            "rapid": 0,
            "laser": 0,
        },
    }
