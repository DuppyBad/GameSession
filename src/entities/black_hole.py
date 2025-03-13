import pygame
import math
import random


class BlackHole:
    def __init__(self, screen_width, screen_height):
        self.radius = 30
        self.max_radius = 80
        self.pos = pygame.Vector2(
            random.randint(screen_width // 4, screen_width * 3 // 4),
            random.randint(100, 200),
        )
        self.attraction_force = 150  # Increased initial force
        self.max_attraction = 400  # Increased maximum force
        self.active = False  # Start active immediately
        self.pulse_speed = 5
        self.current_pulse = 0
        self.growing = True
        self.crushing_entities = []  # List to store entities being crushed

    def update(self, dt, player, platforms, fire_pit):
        if not self.active:
            return

        # Increase size and attraction force gradually
        if self.radius < self.max_radius:
            self.radius += 2 * dt
            self.attraction_force += 20 * dt
            if self.attraction_force > self.max_attraction:
                self.attraction_force = self.max_attraction

        # Apply force to player
        self._apply_force_to_player(dt, player)

        # Apply force to platforms
        for platform in platforms[:]:
            self._apply_force_to_platform(dt, platform)
            # Check if platform is inside black hole
            if self._is_entity_inside(
                platform.rect.centerx, platform.rect.centery, platform.rect.width / 2
            ):
                # Add to crushing entities if not already there
                if platform not in self.crushing_entities:
                    self.crushing_entities.append(
                        {
                            "entity": platform,
                            "type": "platform",
                            "scale": 1.0,
                            "original_size": platform.rect.width,
                        }
                    )

        # Apply force to fire pit
        self._apply_force_to_fire_pit(dt, fire_pit)
        # Check if fire pit is inside black hole
        if self._is_entity_inside(
            fire_pit.rect.centerx, fire_pit.rect.centery, fire_pit.rect.width / 2
        ):
            if fire_pit not in [e["entity"] for e in self.crushing_entities]:
                self.crushing_entities.append(
                    {
                        "entity": fire_pit,
                        "type": "fire_pit",
                        "scale": 1.0,
                        "original_size": fire_pit.rect.width,
                    }
                )

        # Check if player is inside black hole
        if self._is_entity_inside(player.pos.x, player.pos.y, player.size):
            if player not in [e["entity"] for e in self.crushing_entities]:
                self.crushing_entities.append(
                    {
                        "entity": player,
                        "type": "player",
                        "scale": 1.0,
                        "original_size": player.size,
                    }
                )

        # Update crushing animation
        self._update_crushing_animation(dt, platforms, fire_pit, player)

        # Animate pulsing effect
        if self.growing:
            self.current_pulse += self.pulse_speed * dt
            if self.current_pulse >= 20:
                self.growing = False
        else:
            self.current_pulse -= self.pulse_speed * dt
            if self.current_pulse <= 0:
                self.growing = True

    def _is_entity_inside(self, x, y, size):
        distance = math.sqrt((x - self.pos.x) ** 2 + (y - self.pos.y) ** 2)
        return distance < self.radius - size / 2

    def _update_crushing_animation(self, dt, platforms, fire_pit, player):
        # Update each crushing entity
        for i in range(len(self.crushing_entities) - 1, -1, -1):
            entity_data = self.crushing_entities[i]
            entity_data["scale"] -= 2.0 * dt  # Shrink effect

            if entity_data["scale"] <= 0.1:
                # Remove entity if it's completely crushed
                if entity_data["type"] == "platform":
                    if entity_data["entity"] in platforms:
                        platforms.remove(entity_data["entity"])
                elif entity_data["type"] == "fire_pit":
                    fire_pit.active = False
                elif entity_data["type"] == "player":
                    player.size = 0  # Hide player

                self.crushing_entities.pop(i)
            else:
                # Update entity size during crushing
                if entity_data["type"] == "platform":
                    new_width = int(entity_data["original_size"] * entity_data["scale"])
                    new_height = int(
                        entity_data["entity"].rect.height * entity_data["scale"]
                    )
                    entity_data["entity"].rect.width = max(new_width, 1)
                    entity_data["entity"].rect.height = max(new_height, 1)
                elif entity_data["type"] == "fire_pit":
                    new_width = int(entity_data["original_size"] * entity_data["scale"])
                    new_height = int(
                        entity_data["entity"].rect.height * entity_data["scale"]
                    )
                    entity_data["entity"].rect.width = max(new_width, 1)
                    entity_data["entity"].rect.height = max(new_height, 1)
                elif entity_data["type"] == "player":
                    entity_data["entity"].size = max(
                        int(entity_data["original_size"] * entity_data["scale"]), 1
                    )

    def _apply_force_to_player(self, dt, player):
        direction = pygame.Vector2(self.pos.x - player.pos.x, self.pos.y - player.pos.y)
        distance = max(direction.length(), 1)  # Avoid division by zero

        if distance > 0:
            direction = direction / distance
            force_magnitude = self.attraction_force * (1 / max(distance / 300, 0.5))

            player.vel.x += direction.x * force_magnitude * dt
            player.vel.y += direction.y * force_magnitude * dt

    def _apply_force_to_platform(self, dt, platform):
        platform_center_x = platform.rect.centerx
        platform_center_y = platform.rect.centery

        direction_x = self.pos.x - platform_center_x
        direction_y = self.pos.y - platform_center_y
        distance = max(math.sqrt(direction_x**2 + direction_y**2), 1)

        if distance > 0:
            direction_x /= distance
            direction_y /= distance
            force_magnitude = (
                self.attraction_force * 0.3 * (1 / max(distance / 400, 0.5))
            )

            platform.rect.x += int(direction_x * force_magnitude * dt)
            platform.rect.y += int(direction_y * force_magnitude * dt)

    def _apply_force_to_fire_pit(self, dt, fire_pit):
        fire_center_x = fire_pit.rect.centerx
        fire_center_y = fire_pit.rect.centery

        direction_x = self.pos.x - fire_center_x
        direction_y = self.pos.y - fire_center_y
        distance = max(math.sqrt(direction_x**2 + direction_y**2), 1)

        if distance > 0:
            direction_x /= distance
            direction_y /= distance
            force_magnitude = (
                self.attraction_force * 0.3 * (1 / max(distance / 400, 0.5))
            )

            fire_pit.rect.x += int(direction_x * force_magnitude * dt)
            fire_pit.rect.y += int(direction_y * force_magnitude * dt)

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
