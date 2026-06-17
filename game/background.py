import random

import pygame

from settings import HEIGHT, WIDTH


def create_nebula_layer(width, height, colors, cloud_count, seed):
    random_generator = random.Random(seed)
    layer = pygame.Surface((width, height), pygame.SRCALPHA)

    for _ in range(cloud_count):
        x = random_generator.randint(-80, width + 80)
        y = random_generator.randint(-80, height + 80)
        radius = random_generator.randint(70, 190)
        color = random_generator.choice(colors)

        for step in range(5, 0, -1):
            step_radius = int(radius * step / 5)
            alpha = int(7 + step * 4)
            pygame.draw.circle(layer, (*color, alpha), (x, y), step_radius)

    for _ in range(cloud_count * 3):
        x = random_generator.randint(0, width)
        y = random_generator.randint(0, height)
        radius = random_generator.randint(8, 28)
        color = random_generator.choice(colors)
        pygame.draw.circle(layer, (*color, 18), (x, y), radius)

    return layer


def draw_tiled_layer(screen, layer, offset_x):
    width = layer.get_width()
    x = -int(offset_x) % width

    screen.blit(layer, (x - width, 0))
    screen.blit(layer, (x, 0))


def create_nebula_layers():
    return [
        {
            "surface": create_nebula_layer(
                WIDTH,
                HEIGHT,
                [(90, 70, 200), (170, 60, 180), (50, 130, 220)],
                18,
                12
            ),
            "offset": 0,
            "speed": 0.18,
        },
        {
            "surface": create_nebula_layer(
                WIDTH,
                HEIGHT,
                [(255, 95, 120), (120, 220, 210), (245, 170, 70)],
                10,
                42
            ),
            "offset": WIDTH // 3,
            "speed": 0.35,
        },
    ]


def create_stars():
    return [
        [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)]
        for _ in range(120)
    ]


def draw_background(screen, nebula_layers, stars):
    screen.fill((4, 4, 18))

    for nebula in nebula_layers:
        nebula["offset"] += nebula["speed"]
        draw_tiled_layer(screen, nebula["surface"], nebula["offset"])

    for star in stars:
        star[0] -= star[2]

        if star[0] < 0:
            star[0] = WIDTH
            star[1] = random.randint(0, HEIGHT)

        pygame.draw.circle(screen, (220, 220, 220), (star[0], star[1]), star[2])
