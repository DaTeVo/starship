import asyncio

import pygame

from background import create_theme_state, draw_background
from boss import draw_boss, draw_boss_bombs, update_boss
from collisions import handle_collisions
from effects import draw_explosion, update_explosions
from enemies import draw_enemy, update_enemies
from player import draw_ship, update_player
from powerups import draw_powerup, update_powerups
from projectiles import draw_projectiles, update_projectiles
from settings import EXPLOSION_MAX_AGE, FPS, HEIGHT, WIDTH
from state import reset_game
from ui import draw_game_over, draw_hud


async def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Game Python")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 80)

    game = reset_game()
    background = create_theme_state(0)

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
            update_player(game, keys)
            update_enemies(game)
            update_boss(game)
            update_projectiles(game)
            update_powerups(game)
            handle_collisions(game)

        update_explosions(game)

        draw_background(screen, background, game["score"])
        draw_projectiles(screen, game)
        draw_boss_bombs(screen, game)

        for powerup in game["powerups"]:
            draw_powerup(screen, powerup[0], powerup[1], powerup[2], small_font)

        for enemy in game["enemies"]:
            draw_enemy(screen, enemy[0], enemy[1])

        if game["boss"] is not None:
            draw_boss(screen, game["boss"], small_font)

        for explosion in game["explosions"]:
            draw_explosion(
                screen,
                explosion[0],
                explosion[1],
                explosion[2],
                EXPLOSION_MAX_AGE
            )

        draw_ship(screen, game["ship_x"], game["ship_y"])
        draw_hud(screen, game, font, small_font)

        if game["game_over"]:
            draw_game_over(screen, game["score"], big_font, font)

        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
