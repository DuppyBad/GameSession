import pygame


def init_pygame(width, height):
    """Initialize pygame and return the screen and clock objects"""
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    return screen, clock


def create_game_platforms():
    """Create and return the list of platforms for the game"""
    from entities import Platform

    platforms = [
        Platform(0, 650, 400, 70),  # Ground left
        Platform(650, 650, 630, 70),  # Ground right
        Platform(200, 550, 300, 20),
        Platform(600, 450, 300, 20),
        Platform(300, 350, 200, 20),
        Platform(700, 250, 300, 20),
        Platform(100, 150, 200, 20),
    ]
    return platforms


def create_fire_pit():
    """Create and return the fire pit object"""
    from entities import FirePit

    return FirePit(400, 650, 250, 70)


def render_text(screen, text, font, color, position):
    """Render text on the screen at the given position"""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def render_game_over(screen, game_font, width, height):
    """Render the game over text"""
    from constants import RED, WHITE

    game_over_text = game_font.render("Ow ow ow fire...", True, RED)
    respawn_text = game_font.render("Respawning...", True, WHITE)

    screen.blit(
        game_over_text,
        (width // 2 - game_over_text.get_width() // 2, height // 2 - 50),
    )
    screen.blit(
        respawn_text,
        (width // 2 - respawn_text.get_width() // 2, height // 2 + 10),
    )


def render_counter(screen, counter_font, counter, width):
    """Render the movement counter"""
    from constants import WHITE

    counter_text = counter_font.render(f"Moves: {counter}", True, WHITE)
    screen.blit(counter_text, (width - counter_text.get_width() - 20, 20))
