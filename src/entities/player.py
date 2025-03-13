import pygame
from constants import PLAYER_SPEED, JUMP_POWER, GRAVITY, RED


class Player:
    def __init__(self, screen_width, screen_height):
        self.start_pos = pygame.Vector2(screen_width / 4, screen_height / 2)
        self.pos = self.start_pos.copy()
        self.vel = pygame.Vector2(0, 0)
        self.size = 40
        self.on_ground = False
        self.can_jump = False

    def update(self, dt, keys, platforms, screen_width, screen_height):
        # Horizontal movement
        self.vel.x = 0
        if keys[pygame.K_a] and self.pos.x > self.size:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_d] and self.pos.x < screen_width - self.size:
            self.vel.x = PLAYER_SPEED

        # Apply gravity
        self.vel.y += GRAVITY * dt

        # Move player horizontally
        self.pos.x += self.vel.x * dt

        # Check horizontal collisions
        player_rect = self.get_rect()

        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if self.vel.x > 0:  # Moving right
                    self.pos.x = platform.rect.left - self.size
                elif self.vel.x < 0:  # Moving left
                    self.pos.x = platform.rect.right + self.size

        # Move player vertically
        self.pos.y += self.vel.y * dt

        # Update player rectangle after vertical movement
        player_rect = self.get_rect()

        # Check vertical collisions and handle landing on platforms
        self.on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if self.vel.y > 0:  # Falling
                    self.pos.y = platform.rect.top - self.size
                    self.vel.y = 0
                    self.on_ground = True
                    self.can_jump = True
                elif self.vel.y < 0:  # Jumping up
                    self.pos.y = platform.rect.bottom + self.size
                    self.vel.y = 0

        # Screen boundaries check
        if self.pos.x < self.size:
            self.pos.x = self.size
        if self.pos.x > screen_width - self.size:
            self.pos.x = screen_width - self.size
        if self.pos.y < self.size:
            self.pos.y = self.size
            self.vel.y = 0
        if self.pos.y > screen_height - self.size:
            self.pos.y = screen_height - self.size
            self.vel.y = 0
            self.on_ground = True
            self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.vel.y = JUMP_POWER
            self.can_jump = False

    def reset(self):
        self.pos = self.start_pos.copy()
        self.vel = pygame.Vector2(0, 0)

    def get_rect(self):
        return pygame.Rect(
            self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2
        )

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.pos.x), int(self.pos.y)), self.size)
