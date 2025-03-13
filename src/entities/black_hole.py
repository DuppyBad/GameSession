# Spawns a black hole to pull the player into it slowly
import pygame
import random


class BlackHole:
    def __init__(self, screen_width, screen_height):
        self.radius = 30
        self.max_radius = 80
        self.pos = pygame.Vector2(
            random.randint(screen_width // 4, screen_width * 3 // 4),
            random.randint(100, 200),
        )
        self.attraction_force = 100  # Initial force
        self.max_attraction = 300  # Maximum force
        self.spawn_time = 30  # Seconds until spawning
        self.active = False
        self.pulse_speed = 5
        self.current_pulse = 0
        self.growing = True

    def update(self, dt, elapsed_time, player):
        # Check if it's time to activate
        if not self.active and elapsed_time >= self.spawn_time:
            self.active = True

        # Only apply attraction when active
        if self.active:
            # Increase size and attraction force gradually
            if self.radius < self.max_radius:
                self.radius += 2 * dt
                self.attraction_force += 20 * dt
                if self.attraction_force > self.max_attraction:
                    self.attraction_force = self.max_attraction

            # Calculate direction to black hole
            direction = pygame.Vector2(
                self.pos.x - player.pos.x, self.pos.y - player.pos.y
            )
            distance = max(direction.length(), 1)  # Avoid division by zero, very scary

            # Normalize and scale by attraction force (stronger as you get closer)
            if distance > 0:
                direction = direction / distance
                force_magnitude = self.attraction_force * (1 / max(distance / 300, 0.5))

                # Apply force to player
                player.vel.x += direction.x * force_magnitude * dt
                player.vel.y += direction.y * force_magnitude * dt

            # Animate pulsing effect
            if self.growing:
                self.current_pulse += self.pulse_speed * dt
                if self.current_pulse >= 20:
                    self.growing = False
            else:
                self.current_pulse -= self.pulse_speed * dt
                if self.current_pulse <= 0:
                    self.growing = True

    def draw(self, screen):
        if not self.active:
            return

        # Draw outer glow (pulsing)
        pulse_radius = self.radius + self.current_pulse
        pygame.draw.circle(
            screen,
            (100, 0, 150, 128),
            (int(self.pos.x), int(self.pos.y)),
            int(pulse_radius * 1.5),
        )

        # Draw main black hole
        pygame.draw.circle(
            screen, (20, 0, 30), (int(self.pos.x), int(self.pos.y)), int(self.radius)
        )

        # Draw center accretion disk
        pygame.draw.circle(
            screen,
            (150, 50, 200),
            (int(self.pos.x), int(self.pos.y)),
            int(self.radius * 0.4),
        )
