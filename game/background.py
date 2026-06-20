import random

import pygame

from settings import BACKGROUND_SCORE_STEP, HEIGHT, WIDTH


THEMES = [
    "nebula",
    "deep_space",
    "volcanic_planet",
    "supernova",
    "crystal_field",
]


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
                12,
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
                42,
            ),
            "offset": WIDTH // 3,
            "speed": 0.35,
        },
    ]


def create_stars(count=180, seed=None):
    random_generator = random.Random(seed)

    return [
        {
            "x": random_generator.randint(0, WIDTH),
            "y": random_generator.randint(0, HEIGHT),
            "size": random_generator.randint(1, 3),
            "speed": random_generator.uniform(0.7, 2.8),
            "brightness": random_generator.randint(155, 255),
        }
        for _ in range(count)
    ]


def create_planets(theme, seed):
    random_generator = random.Random(seed)
    planets = []
    planet_count = 2 if theme == "nebula" else 3

    for _ in range(planet_count):
        radius = random_generator.randint(22, 70)
        planets.append({
            "x": random_generator.randint(0, WIDTH),
            "y": random_generator.randint(70, HEIGHT - 70),
            "radius": radius,
            "speed": random_generator.uniform(0.12, 0.45),
            "color": random_generator.choice(theme_planet_colors(theme)),
            "ring": random_generator.random() < 0.35,
        })

    return planets


def create_debris(theme, seed):
    random_generator = random.Random(seed)

    return [
        {
            "x": random_generator.randint(0, WIDTH),
            "y": random_generator.randint(0, HEIGHT),
            "size": random_generator.randint(7, 22),
            "speed": random_generator.uniform(0.55, 1.6),
            "angle": random_generator.randint(0, 360),
            "color": random_generator.choice(theme_debris_colors(theme)),
        }
        for _ in range(32)
    ]


def create_theme_state(theme_index):
    theme = THEMES[theme_index % len(THEMES)]

    return {
        "theme_index": theme_index,
        "theme": theme,
        "stars": create_stars(theme_star_count(theme), theme_index * 71 + 8),
        "planets": create_planets(theme, theme_index * 97 + 11),
        "debris": create_debris(theme, theme_index * 43 + 19),
        "nebula_layers": create_theme_nebula_layers(theme, theme_index),
        "supernova_pulse": 0,
    }


def create_theme_nebula_layers(theme, theme_index):
    palettes = {
        "nebula": [
            [(90, 70, 200), (170, 60, 180), (50, 130, 220)],
            [(255, 95, 120), (120, 220, 210), (245, 170, 70)],
        ],
        "deep_space": [
            [(25, 40, 85), (50, 80, 135), (20, 110, 150)],
            [(90, 120, 190), (40, 180, 210), (35, 55, 110)],
        ],
        "volcanic_planet": [
            [(170, 35, 20), (210, 80, 25), (95, 25, 40)],
            [(255, 135, 40), (190, 45, 20), (110, 20, 20)],
        ],
        "supernova": [
            [(255, 210, 90), (255, 115, 70), (150, 70, 210)],
            [(255, 245, 190), (250, 80, 120), (120, 130, 255)],
        ],
        "crystal_field": [
            [(60, 170, 200), (120, 220, 255), (80, 90, 190)],
            [(180, 235, 255), (95, 210, 190), (110, 125, 245)],
        ],
    }

    first, second = palettes[theme]

    return [
        {
            "surface": create_nebula_layer(WIDTH, HEIGHT, first, 14, theme_index * 100 + 12),
            "offset": 0,
            "speed": 0.16,
        },
        {
            "surface": create_nebula_layer(WIDTH, HEIGHT, second, 9, theme_index * 100 + 42),
            "offset": WIDTH // 3,
            "speed": 0.31,
        },
    ]


def theme_star_count(theme):
    counts = {
        "nebula": 230,
        "deep_space": 320,
        "volcanic_planet": 190,
        "supernova": 260,
        "crystal_field": 240,
    }
    return counts[theme]


def theme_base_color(theme):
    colors = {
        "nebula": (4, 4, 18),
        "deep_space": (1, 3, 12),
        "volcanic_planet": (18, 4, 5),
        "supernova": (20, 10, 28),
        "crystal_field": (4, 12, 24),
    }
    return colors[theme]


def theme_planet_colors(theme):
    colors = {
        "nebula": [(40, 90, 170), (120, 80, 170), (210, 115, 85)],
        "deep_space": [(45, 65, 105), (95, 110, 150), (45, 120, 135)],
        "volcanic_planet": [(180, 45, 25), (230, 95, 25), (95, 45, 35)],
        "supernova": [(255, 190, 80), (235, 85, 120), (160, 100, 255)],
        "crystal_field": [(100, 210, 230), (160, 240, 255), (95, 125, 240)],
    }
    return colors[theme]


def theme_debris_colors(theme):
    colors = {
        "nebula": [(95, 100, 130), (130, 110, 160), (80, 120, 150)],
        "deep_space": [(65, 75, 95), (85, 100, 125), (45, 55, 80)],
        "volcanic_planet": [(120, 45, 30), (190, 75, 35), (70, 45, 45)],
        "supernova": [(255, 180, 80), (215, 80, 120), (130, 95, 220)],
        "crystal_field": [(95, 210, 235), (170, 240, 255), (110, 130, 230)],
    }
    return colors[theme]


def draw_background(screen, background, score):
    theme_index = score // BACKGROUND_SCORE_STEP

    if background["theme_index"] != theme_index:
        background.clear()
        background.update(create_theme_state(theme_index))

    screen.fill(theme_base_color(background["theme"]))
    draw_nebula(screen, background)
    draw_special_sky(screen, background)
    draw_stars(screen, background["stars"])
    draw_planets(screen, background["planets"])
    draw_debris(screen, background)


def draw_nebula(screen, background):
    for nebula in background["nebula_layers"]:
        nebula["offset"] += nebula["speed"]
        draw_tiled_layer(screen, nebula["surface"], nebula["offset"])


def draw_special_sky(screen, background):
    theme = background["theme"]

    if theme == "supernova":
        background["supernova_pulse"] = (background["supernova_pulse"] + 1) % 120
        pulse = abs(60 - background["supernova_pulse"])
        radius = 120 + pulse
        pygame.draw.circle(screen, (255, 210, 95), (WIDTH - 170, 120), radius)
        pygame.draw.circle(screen, (255, 245, 190), (WIDTH - 170, 120), radius // 2)

    if theme == "volcanic_planet":
        pygame.draw.circle(screen, (115, 25, 15), (WIDTH - 150, HEIGHT + 105), 220)
        pygame.draw.circle(screen, (230, 80, 20), (WIDTH - 220, HEIGHT - 20), 18)
        pygame.draw.circle(screen, (255, 170, 50), (WIDTH - 220, HEIGHT - 20), 8)


def draw_stars(screen, stars):
    for star in stars:
        star["x"] -= star["speed"]

        if star["x"] < 0:
            star["x"] = WIDTH
            star["y"] = random.randint(0, HEIGHT)

        shade = star["brightness"]
        pygame.draw.circle(
            screen,
            (shade, shade, min(255, shade + 20)),
            (int(star["x"]), int(star["y"])),
            star["size"],
        )


def draw_planets(screen, planets):
    for planet in planets:
        planet["x"] -= planet["speed"]

        if planet["x"] < -planet["radius"] * 2:
            planet["x"] = WIDTH + planet["radius"] * 2
            planet["y"] = random.randint(70, HEIGHT - 70)

        x = int(planet["x"])
        y = int(planet["y"])
        radius = planet["radius"]
        color = planet["color"]
        shadow = tuple(max(0, channel - 55) for channel in color)

        pygame.draw.circle(screen, shadow, (x + 7, y + 5), radius)
        pygame.draw.circle(screen, color, (x, y), radius)
        pygame.draw.circle(screen, (255, 255, 255), (x - radius // 3, y - radius // 3), max(3, radius // 8))

        if planet["ring"]:
            ring_rect = pygame.Rect(x - radius - 18, y - radius // 3, radius * 2 + 36, int(radius / 1.5))
            pygame.draw.ellipse(screen, (210, 210, 220), ring_rect, 2)


def draw_debris(screen, background):
    if background["theme"] not in ("volcanic_planet", "crystal_field", "deep_space"):
        return

    for debris in background["debris"]:
        debris["x"] -= debris["speed"]
        debris["angle"] = (debris["angle"] + 1) % 360

        if debris["x"] < -40:
            debris["x"] = WIDTH + random.randint(0, 140)
            debris["y"] = random.randint(0, HEIGHT)

        draw_debris_piece(screen, debris)


def draw_debris_piece(screen, debris):
    x = int(debris["x"])
    y = int(debris["y"])
    size = debris["size"]

    points = [
        (x - size, y),
        (x - size // 3, y - size),
        (x + size, y - size // 2),
        (x + size // 2, y + size),
        (x - size // 2, y + size // 2),
    ]

    pygame.draw.polygon(screen, debris["color"], points)
    pygame.draw.polygon(screen, (230, 230, 240), points, 1)
