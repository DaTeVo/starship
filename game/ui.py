import pygame

from settings import FPS, HEIGHT, POWER_NAMES, WIDTH


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


def draw_hud(screen, game, font, small_font):
    score_text = font.render(f"Score : {game['score']}", True, (255, 255, 255))
    life_text = font.render(f"Vie : {game['player_life']}", True, (255, 255, 255))
    bonus_text = font.render(f"Bonus : {game['bonus_life']}", True, (255, 220, 40))

    screen.blit(score_text, (20, 20))
    screen.blit(life_text, (20, 55))
    screen.blit(bonus_text, (20, 90))

    y_power = 125

    for power_type, timer in game["power_timers"].items():
        if timer > 0:
            seconds_left = timer // FPS + 1
            power_text = small_font.render(
                f"{POWER_NAMES[power_type]} : {seconds_left}s", True, (255, 255, 255)
            )

            screen.blit(power_text, (20, y_power))
            y_power += 25
