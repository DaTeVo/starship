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

    # Flamme moteur
    flame = [
        (x - 20, y - 8),
        (x - 38, y),
        (x - 20, y + 8),
    ]
    pygame.draw.polygon(screen, (255, 120, 40), flame)


async def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Game Python")
    clock = pygame.time.Clock()

    ship_x = WIDTH // 2
    ship_y = HEIGHT // 2
    speed = 5

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

        screen.fill((5, 5, 20))

        # Défilement des étoiles
        for star in stars:
            star[0] -= star[2]
            if star[0] < 0:
                star[0] = WIDTH
                star[1] = random.randint(0, HEIGHT)

            pygame.draw.circle(screen, (220, 220, 220), (star[0], star[1]), star[2])

        draw_ship(screen, ship_x, ship_y)

        pygame.display.flip()

        # Obligatoire pour pygbag / navigateur
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
