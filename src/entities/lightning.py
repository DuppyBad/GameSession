import pygame
import math
import time
import random
from constants import WHITE, LIGHT_BLUE


class Lightning:
    def __init__(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.strike_time = time.time() + 2.0  # Strike 2 seconds after creation
        self.active = False
        self.flash_duration = 0.2  # How long the flash stays visible
        self.end_time = 0
        self.segments = []
        self.width = 5
        self.warning_circle_size = 0
        self.max_warning_size = 50
        self.hit_radius = 60  # Radius for collision detection

    def update(self, current_time):
        # Warning phase
        if current_time < self.strike_time:
            # Calculate warning circle size (grows as strike approaches)
            progress = (current_time - (self.strike_time - 2.0)) / 2.0
            self.warning_circle_size = int(progress * self.max_warning_size)
        # Strike phase
        elif not self.active and current_time >= self.strike_time:
            self.active = True
            self.end_time = current_time + self.flash_duration

            # Generate lightning segments (zigzag pattern from top of screen to target)
            self.segments = []
            start_x = self.target_x
            start_y = 0
            end_x = self.target_x
            end_y = self.target_y

            segments = 10  # Number of zigzag segments
            current_x = start_x
            current_y = start_y

            for i in range(segments):
                next_y = start_y + (end_y - start_y) * (i + 1) / segments
                # Random horizontal displacement, more pronounced in the middle
                displacement = random.randint(-40, 40)
                if i == segments - 1:  # Last segment points exactly to target
                    next_x = end_x
                else:
                    next_x = current_x + displacement

                self.segments.append((current_x, current_y, next_x, next_y))
                current_x, current_y = next_x, next_y

        # Check if strike has ended
        if self.active and current_time > self.end_time:
            return False  # Lightning is done

        return True  # Lightning is still active

    def draw(self, screen):
        current_time = time.time()

        # Draw warning circle before strike
        if not self.active and current_time < self.strike_time:
            # Warning circle (pulsing)
            pulse = abs(math.sin(current_time * 10)) * 50
            color_value = int(200 + pulse)
            warning_color = (color_value, 0, 0)
            pygame.draw.circle(
                screen,
                warning_color,
                (int(self.target_x), int(self.target_y)),
                self.warning_circle_size,
                2,
            )

        # Draw actual lightning strike
        if self.active and current_time <= self.end_time:
            # Draw main bolt
            for segment in self.segments:
                pygame.draw.line(
                    screen,
                    WHITE,
                    (segment[0], segment[1]),
                    (segment[2], segment[3]),
                    self.width,
                )

            # Draw thinner inner bolt (for glow effect)
            for segment in self.segments:
                pygame.draw.line(
                    screen,
                    LIGHT_BLUE,
                    (segment[0], segment[1]),
                    (segment[2], segment[3]),
                    self.width - 2,
                )

            # Draw flash at impact point
            flash_radius = 80 * ((self.end_time - current_time) / self.flash_duration)
            pygame.draw.circle(
                screen,
                WHITE,
                (int(self.target_x), int(self.target_y)),
                int(flash_radius),
            )
            pygame.draw.circle(
                screen,
                LIGHT_BLUE,
                (int(self.target_x), int(self.target_y)),
                int(flash_radius * 0.7),
            )

    def check_player_hit(self, player_pos):
        current_time = time.time()
        # Only check when lightning is actually striking
        if self.active and current_time <= self.end_time:
            distance = math.sqrt(
                (player_pos.x - self.target_x) ** 2
                + (player_pos.y - self.target_y) ** 2
            )
            return distance < self.hit_radius
        return False
