import random
import time
import pygame
from constants import RESPAWN_DELAY
from entities import Lightning


class GameState:
    def __init__(self):
        self.game_over = False
        self.respawn_timer = 0
        self.movement_counter = 0
        self.last_key_state = {
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_SPACE: False,
        }
        self.lightning_strikes = []

    def check_movement_keys(self, keys, player_pos):
        # Check each movement key
        for key in [pygame.K_a, pygame.K_d, pygame.K_SPACE]:
            # If key is pressed now but wasn't pressed last frame
            if keys[key] and not self.last_key_state[key]:
                # 1/8 chance to increment counter
                if random.randint(1, 8) == 1:
                    self.movement_counter += 1
                    # Create a lightning strike at player's current position
                    self.lightning_strikes.append(Lightning(player_pos.x, player_pos.y))

        # Update last key state
        self.last_key_state[pygame.K_a] = keys[pygame.K_a]
        self.last_key_state[pygame.K_d] = keys[pygame.K_d]
        self.last_key_state[pygame.K_SPACE] = keys[pygame.K_SPACE]

    def check_fire_collision(self, player, fire_pit):
        player_rect = player.get_rect()
        return player_rect.colliderect(fire_pit.rect)

    def check_lightning_collisions(self, player_pos):
        for lightning in self.lightning_strikes[:]:
            if lightning.check_player_hit(player_pos):
                return True
        return False

    def update_lightnings(self, current_time):
        for i in range(len(self.lightning_strikes) - 1, -1, -1):
            if not self.lightning_strikes[i].update(current_time):
                self.lightning_strikes.pop(i)

    def handle_death(self):
        self.game_over = True
        self.respawn_timer = time.time() + RESPAWN_DELAY

    def check_respawn(self, player):
        if self.game_over:
            current_time = time.time()
            if current_time > self.respawn_timer:
                self.restart_game(player)
                return True
        return False

    def restart_game(self, player):
        player.reset()
        self.game_over = False
        self.lightning_strikes = []
