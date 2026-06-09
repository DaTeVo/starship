import asyncio
import random
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


async def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Game Python")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    ship_x = WIDTH // 2
    ship_y = HEIGHT // 2
    speed = 5

    player_life = 3

    bullets = []
    bullet_speed = 10
    shoot_cooldown = 0

    enemy_bullets = []
    enemy_bullet_speed = 6

    enemies = []
    enemy_speed = 3
    spawn_timer = 0

    enemy_shoot_timer = 0

    score = 0

    stars = [
        [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)]
        for _ in range(120)
    ]

    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            ship_x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship_x += speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            ship_y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ship_y += speed

        ship_x = max(30, min(WIDTH - 30, ship_x))
        ship_y = max(30, min(HEIGHT - 30, ship_y))

        # Tir du joueur avec espace
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            bullets.append([ship_x + 30, ship_y])
            shoot_cooldown = 15

        # Apparition des ennemis
        spawn_timer += 1
        if spawn_timer >= 60:
            enemies.append([WIDTH + 40, random.randint(40, HEIGHT - 40)])
            spawn_timer = 0

        # Enemies gunfire
        enemy_shoot_timer += 1

        if enemy_shoot_timer >= 50 and len(enemies) > 0:
            enemy = random.choice(enemies)
            enemy_bullets.append([enemy[0] - 30, enemy[1]])
            enemy_shoot_timer = 0

        # Déplacement des balles du joueur
        for bullet in bullets:
            bullet[0] += bullet_speed

        bullets = [bullet for bullet in bullets if bullet[0] < WIDTH + 20]

        # Déplacement des balles ennemies
        for enemy_bullet in enemy_bullets:
            enemy_bullet[0] -= enemy_bullet_speed

        enemy_bullets = [
            enemy_bullet for enemy_bullet in enemy_bullets
            if enemy_bullet[0] > -20
        ]

        # Déplacement des ennemis
        for enemy in enemies:
            enemy[0] -= enemy_speed

        enemies = [enemy for enemy in enemies if enemy[0] > -50]

        # Collisions balles du joueur / ennemis
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1] - 3, 12, 6)

            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy[0] - 25, enemy[1] - 15, 50, 30)

                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # Gunfire collision enemies -> player
        player_rect = pygame.Rect(ship_x - 25, ship_y - 15, 50, 30)

        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet_rect = pygame.Rect(enemy_bullet[0], enemy_bullet[1] - 3, 12, 6)

            if enemy_bullet_rect.colliderect(player_rect):
                enemy_bullets.remove(enemy_bullet)
                player_life -= 1

                if player_life <= 0:
                    running = False

        screen.fill((5, 5, 20))

        # Stars
        for star in stars:
            star[0] -= star[2]

            if star[0] < 0:
                star[0] = WIDTH
                star[1] = random.randint(0, HEIGHT)

            pygame.draw.circle(screen, (220, 220, 220), (star[0], star[1]), star[2])

        # Player gunfire
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 80), (bullet[0], bullet[1] - 3, 12, 6))

        # Enemies gunfire
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(
                screen,
                (255, 80, 80),
                (enemy_bullet[0], enemy_bullet[1] - 3, 12, 6)
            )

        # Ennemies
        for enemy in enemies:
            draw_enemy(screen, enemy[0], enemy[1])

        draw_ship(screen, ship_x, ship_y)

        score_text = font.render(f"Score : {score}", True, (255, 255, 255))
        life_text = font.render(f"Vie : {player_life}", True, (255, 255, 255))

        screen.blit(score_text, (20, 20))
        screen.blit(life_text, (20, 55))

        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
