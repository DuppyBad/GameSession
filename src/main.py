import pygame
import time
from constants import PURPLE, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from entities import Player, Lightning
from game_state import GameState
from utils import (
    init_pygame,
    create_game_platforms,
    create_fire_pit,
    render_text,
    render_game_over,
    render_counter,
)


def main():
    # Initialize pygame
    screen, clock = init_pygame(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Create game objects
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    platforms = create_game_platforms()
    fire_pit = create_fire_pit()
    game_state = GameState()

    # Main game font
    game_font = pygame.font.SysFont(None, 48)
    counter_font = pygame.font.SysFont(None, 36)

    # Game loop
    running = True
    dt = 0

    while running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_SPACE
                    and player.can_jump
                    and not game_state.game_over
                ):
                    player.jump()
                if event.key == pygame.K_r:  # Restart with R key
                    game_state.restart_game(player)

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Quit with Q key
        if keys[pygame.K_q]:
            running = False

        # Check for movement counter increment
        if not game_state.game_over:
            game_state.check_movement_keys(keys, player.pos)

        # Handle game over and respawn
        if game_state.game_over:
            game_state.check_respawn(player)
        else:
            # Update player
            player.update(dt, keys, platforms, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Check collisions
            if game_state.check_fire_collision(player, fire_pit):
                game_state.handle_death()

            if game_state.check_lightning_collisions(player.pos):
                game_state.handle_death()

        # Update fire animation
        fire_pit.update(dt)

        # Update lightning strikes
        current_time = time.time()
        game_state.update_lightnings(current_time)

        # Fill the screen with background color
        screen.fill(PURPLE)

        # Draw platforms
        for platform in platforms:
            platform.draw(screen)

        # Draw fire pit
        fire_pit.draw(screen)

        # Draw lightning strikes
        for lightning in game_state.lightning_strikes:
            lightning.draw(screen)

        # Draw player (unless game over)
        if not game_state.game_over:
            player.draw(screen)

        # Show game over message
        if game_state.game_over:
            render_game_over(screen, game_font, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Draw movement counter in top right
        render_counter(screen, counter_font, game_state.movement_counter, SCREEN_WIDTH)

        # Flip the display to put work on screen
        pygame.display.flip()

        # Limit FPS
        dt = clock.tick(FPS) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
