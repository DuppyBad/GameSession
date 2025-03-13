import pygame
from constants import ORANGE, YELLOW


class FirePit:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.flame_heights = [0] * (width // 10)  # Store heights for each flame segment
        self.base_height = height

    def update(self, dt):
        # Animate flames
        for i in range(len(self.flame_heights)):
            # Random flickering effect
            self.flame_heights[i] = max(
                0, self.flame_heights[i] + (pygame.time.get_ticks() % 5 - 2)
            )
            # Reset occasionally for variety
            if pygame.time.get_ticks() % 100 < 5:
                self.flame_heights[i] = pygame.time.get_ticks() % 30

    def draw(self, screen):
        # Draw fire base (coals)
        pygame.draw.rect(screen, (150, 30, 30), self.rect)

        # Draw flames
        segment_width = 10
        for i in range(len(self.flame_heights)):
            flame_height = self.flame_heights[i]
            x = self.rect.x + i * segment_width

            # Main flame (orange)
            flame_rect = pygame.Rect(
                x, self.rect.y - flame_height - 15, segment_width, flame_height + 15
            )
            pygame.draw.rect(screen, ORANGE, flame_rect)

            # Inner flame (yellow)
            if flame_height > 5:
                inner_flame_rect = pygame.Rect(
                    x + 2,
                    self.rect.y - flame_height - 10,
                    segment_width - 4,
                    flame_height,
                )
                pygame.draw.rect(screen, YELLOW, inner_flame_rect)
