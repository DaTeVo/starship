import asyncio
import random
import math
import pygame


WIDTH = 960
HEIGHT = 540
FPS = 60


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


def draw_enemy(screen, x, y):
    points = [
        (x - 25, y),
        (x + 20, y - 15),
        (x + 10, y),
        (x + 20, y + 15),
    ]
    pygame.draw.polygon(screen, (255, 80, 80), points)
    pygame.draw.polygon(screen, (255, 180, 180), points, 2)


def draw_powerup(screen, x, y, power_type, font):
    colors = {
        "triple": (180, 100, 255),
        "rapid": (100, 255, 120),
        "laser": (80, 220, 255),
    }

    letters = {
        "triple": "T",
        "rapid": "R",
        "laser": "L",
    }

    color = colors[power_type]
    letter = letters[power_type]

    pygame.draw.circle(screen, color, (x, y), 14)
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 14, 2)

    text = font.render(letter, True, (10, 10, 20))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


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


def draw_game_over(screen, score, big_font, font):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title = big_font.render("GAME OVER", True, (255, 80, 80))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(title, title_rect)

    score_text = font.render(f"Score final : {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Appuie sur R pour recommencer", True, (220, 220, 220))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(restart_text, restart_rect)

    quit_text = font.render("Appuie sur ECHAP pour quitter", True, (180, 180, 180))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 65))
    screen.blit(quit_text, quit_rect)


async def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Game Python")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 80)

    speed = 5
    bullet_speed = 10
    enemy_bullet_speed = 6
    enemy_speed = 3

    powerup_duration = 8 * FPS
    explosion_max_age = 25

    def reset_game():
        return {
            "ship_x": WIDTH // 2,
            "ship_y": HEIGHT // 2,
            "player_life": 3,
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

    game = reset_game()

    stars = [
        [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)]
        for _ in range(120)
    ]

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game["game_over"] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = reset_game()

                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        if not game["game_over"]:
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                game["ship_x"] -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                game["ship_x"] += speed
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                game["ship_y"] -= speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                game["ship_y"] += speed

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

            cooldown_time = 5 if rapid_is_active else 15
            bullet_type = "laser" if laser_is_active else "normal"

            if keys[pygame.K_SPACE] and game["shoot_cooldown"] == 0:
                if triple_is_active:
                    game["bullets"].append([game["ship_x"] + 30, game["ship_y"] - 12, bullet_type])
                    game["bullets"].append([game["ship_x"] + 30, game["ship_y"], bullet_type])
                    game["bullets"].append([game["ship_x"] + 30, game["ship_y"] + 12, bullet_type])
                else:
                    game["bullets"].append([game["ship_x"] + 30, game["ship_y"], bullet_type])

                game["shoot_cooldown"] = cooldown_time

            game["spawn_timer"] += 1
            if game["spawn_timer"] >= 60:
                game["enemies"].append([WIDTH + 40, random.randint(40, HEIGHT - 40)])
                game["spawn_timer"] = 0

            game["enemy_shoot_timer"] += 1

            if game["enemy_shoot_timer"] >= 50 and len(game["enemies"]) > 0:
                enemy = random.choice(game["enemies"])
                game["enemy_bullets"].append([enemy[0] - 30, enemy[1]])
                game["enemy_shoot_timer"] = 0

            for bullet in game["bullets"]:
                if bullet[2] == "laser":
                    bullet[0] += bullet_speed + 3
                else:
                    bullet[0] += bullet_speed

            game["bullets"] = [
                bullet for bullet in game["bullets"]
                if bullet[0] < WIDTH + 40
            ]

            for enemy_bullet in game["enemy_bullets"]:
                enemy_bullet[0] -= enemy_bullet_speed

            game["enemy_bullets"] = [
                enemy_bullet for enemy_bullet in game["enemy_bullets"]
                if enemy_bullet[0] > -20
            ]

            for enemy in game["enemies"]:
                enemy[0] -= enemy_speed

            game["enemies"] = [
                enemy for enemy in game["enemies"]
                if enemy[0] > -50
            ]

            for powerup in game["powerups"]:
                powerup[0] -= 3

            game["powerups"] = [
                powerup for powerup in game["powerups"]
                if powerup[0] > -30
            ]

            for bullet in game["bullets"][:]:
                if bullet[2] == "laser":
                    bullet_rect = pygame.Rect(bullet[0], bullet[1] - 6, 26, 12)
                else:
                    bullet_rect = pygame.Rect(bullet[0], bullet[1] - 3, 12, 6)

                for enemy in game["enemies"][:]:
                    enemy_rect = pygame.Rect(enemy[0] - 25, enemy[1] - 15, 50, 30)

                    if bullet_rect.colliderect(enemy_rect):
                        game["enemies"].remove(enemy)
                        game["explosions"].append([enemy[0], enemy[1], 0])
                        game["score"] += 1

                        if random.random() < 0.25:
                            power_type = random.choice(["triple", "rapid", "laser"])
                            game["powerups"].append([enemy[0], enemy[1], power_type])

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
                enemy_bullet_rect = pygame.Rect(enemy_bullet[0], enemy_bullet[1] - 3, 12, 6)

                if enemy_bullet_rect.colliderect(player_rect):
                    game["enemy_bullets"].remove(enemy_bullet)
                    game["player_life"] -= 1

                    if game["player_life"] <= 0:
                        game["game_over"] = True

            for enemy in game["enemies"][:]:
                enemy_rect = pygame.Rect(enemy[0] - 25, enemy[1] - 15, 50, 30)

                if player_rect.colliderect(enemy_rect):
                    game["enemies"].remove(enemy)
                    game["explosions"].append([enemy[0], enemy[1], 0])
                    game["player_life"] -= 1

                    if game["player_life"] <= 0:
                        game["game_over"] = True

            for powerup in game["powerups"][:]:
                powerup_rect = pygame.Rect(powerup[0] - 14, powerup[1] - 14, 28, 28)

                if player_rect.colliderect(powerup_rect):
                    game["powerups"].remove(powerup)
                    game["power_timers"][powerup[2]] = powerup_duration

        for explosion in game["explosions"]:
            explosion[2] += 1

        game["explosions"] = [
            explosion for explosion in game["explosions"]
            if explosion[2] <= explosion_max_age
        ]

        screen.fill((5, 5, 20))

        for star in stars:
            star[0] -= star[2]

            if star[0] < 0:
                star[0] = WIDTH
                star[1] = random.randint(0, HEIGHT)

            pygame.draw.circle(screen, (220, 220, 220), (star[0], star[1]), star[2])

        for bullet in game["bullets"]:
            if bullet[2] == "laser":
                pygame.draw.rect(screen, (80, 220, 255), (bullet[0], bullet[1] - 6, 26, 12))
                pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1] - 2, 26, 4))
            else:
                pygame.draw.rect(screen, (255, 255, 80), (bullet[0], bullet[1] - 3, 12, 6))

        for enemy_bullet in game["enemy_bullets"]:
            pygame.draw.rect(
                screen,
                (255, 80, 80),
                (enemy_bullet[0], enemy_bullet[1] - 3, 12, 6)
            )

        for powerup in game["powerups"]:
            draw_powerup(screen, powerup[0], powerup[1], powerup[2], small_font)

        for enemy in game["enemies"]:
            draw_enemy(screen, enemy[0], enemy[1])

        for explosion in game["explosions"]:
            draw_explosion(
                screen,
                explosion[0],
                explosion[1],
                explosion[2],
                explosion_max_age
            )

        draw_ship(screen, game["ship_x"], game["ship_y"])

        score_text = font.render(f"Score : {game['score']}", True, (255, 255, 255))
        life_text = font.render(f"Vie : {game['player_life']}", True, (255, 255, 255))

        screen.blit(score_text, (20, 20))
        screen.blit(life_text, (20, 55))

        y_power = 90
        power_names = {
            "triple": "Triple tir",
            "rapid": "Tir rapide",
            "laser": "Laser",
        }

        for power_type, timer in game["power_timers"].items():
            if timer > 0:
                seconds_left = timer // FPS + 1
                power_text = small_font.render(
                    f"{power_names[power_type]} : {seconds_left}s",
                    True,
                    (255, 255, 255)
                )
                screen.blit(power_text, (20, y_power))
                y_power += 25

        if game["game_over"]:
            draw_game_over(screen, game["score"], big_font, font)

        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
