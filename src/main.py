import pygame
import math
import time
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Game constants
GRAVITY = 1200  # Increased for delta time
JUMP_POWER = -600
PLAYER_SPEED = 300

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Game state
game_over = False
respawn_timer = 0
respawn_delay = 1.5  # seconds

# Movement counter
movement_counter = 0
last_key_state = {pygame.K_a: False, pygame.K_d: False, pygame.K_SPACE: False}

# Player setup
player_start_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 2)
player_pos = player_start_pos.copy()
player_vel = pygame.Vector2(0, 0)
player_size = 40
on_ground = False
# Maybe edit later on for double jump type abilities
can_jump = False  # To prevent multi-jumping


# Lightning system
class Lightning:
    # Maybe doesn't have to be a class? Seems easier for now
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

    def draw(self):
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


# Lightning list
lightning_strikes = []


# Platform class
class Platform:
    def __init__(self, x, y, width, height, color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


# Fire pit class
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

    def draw(self):
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


# Create platforms
# Picked sort of random values for this, definitely needs to be adjusted
platforms = [
    Platform(0, 650, 400, 70),  # Ground left
    Platform(650, 650, 630, 70),  # Ground right
    Platform(200, 550, 300, 20),
    Platform(600, 450, 300, 20),
    Platform(300, 350, 200, 20),
    Platform(700, 250, 300, 20),
    Platform(100, 150, 200, 20),
]

# Create fire pit
fire_pit = FirePit(400, 650, 250, 70)


def restart_game():
    global player_pos, player_vel, game_over, lightning_strikes
    player_pos = player_start_pos.copy()
    player_vel = pygame.Vector2(0, 0)
    game_over = False
    lightning_strikes = []  # Clear any pending lightning strikes


def check_fire_collision():
    player_rect = pygame.Rect(
        player_pos.x - player_size,
        player_pos.y - player_size,
        player_size * 2,
        player_size * 2,
    )
    return player_rect.colliderect(fire_pit.rect)


def check_movement_keys(keys):
    global movement_counter, last_key_state, lightning_strikes

    # Check each movement key
    for key in [pygame.K_a, pygame.K_d, pygame.K_SPACE]:
        # If key is pressed now but wasn't pressed last frame
        if keys[key] and not last_key_state[key]:
            # 1/8 chance to increment counter
            if random.randint(1, 8) == 1:
                movement_counter += 1
                # Create a lightning strike at player's current position
                lightning_strikes.append(Lightning(player_pos.x, player_pos.y))

    # Update last key state
    last_key_state[pygame.K_a] = keys[pygame.K_a]
    last_key_state[pygame.K_d] = keys[pygame.K_d]
    last_key_state[pygame.K_SPACE] = keys[pygame.K_SPACE]


# Main game font
# A pixel art-esque font would work best, ala cozette etc. TODO: Change font
game_font = pygame.font.SysFont(None, 48)
counter_font = pygame.font.SysFont(None, 36)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and can_jump and not game_over:
                player_vel.y = JUMP_POWER
                can_jump = False
            if event.key == pygame.K_r:  # Restart with R key
                restart_game()

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Check for movement counter increment
    if not game_over:
        check_movement_keys(keys)

    # Handle game over and respawn
    if game_over:
        current_time = time.time()
        if current_time > respawn_timer:
            restart_game()
    else:
        # Horizontal movement
        player_vel.x = 0
        if keys[pygame.K_a] and player_pos.x > player_size:
            player_vel.x = -PLAYER_SPEED
        if keys[pygame.K_d] and player_pos.x < screen.get_width() - player_size:
            player_vel.x = PLAYER_SPEED

        # Apply gravity
        player_vel.y += GRAVITY * dt

        # Move player horizontally
        player_pos.x += player_vel.x * dt

        # Check horizontal collisions
        player_rect = pygame.Rect(
            player_pos.x - player_size,
            player_pos.y - player_size,
            player_size * 2,
            player_size * 2,
        )

        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if player_vel.x > 0:  # Moving right
                    player_pos.x = platform.rect.left - player_size
                elif player_vel.x < 0:  # Moving left
                    player_pos.x = platform.rect.right + player_size

        # Move player vertically
        player_pos.y += player_vel.y * dt

        # Update player rectangle after vertical movement
        player_rect = pygame.Rect(
            player_pos.x - player_size,
            player_pos.y - player_size,
            player_size * 2,
            player_size * 2,
        )

        # Check vertical collisions and handle landing on platforms
        on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if player_vel.y > 0:  # Falling
                    player_pos.y = platform.rect.top - player_size
                    player_vel.y = 0
                    on_ground = True
                    can_jump = True
                elif player_vel.y < 0:  # Jumping up
                    player_pos.y = platform.rect.bottom + player_size
                    player_vel.y = 0

        # Check fire pit collision
        if check_fire_collision():
            game_over = True
            respawn_timer = time.time() + respawn_delay

        # Check lightning collisions
        for lightning in lightning_strikes[:]:
            if lightning.check_player_hit(player_pos):
                game_over = True
                respawn_timer = time.time() + respawn_delay

        # Screen boundaries check
        if player_pos.x < player_size:
            player_pos.x = player_size
        if player_pos.x > screen.get_width() - player_size:
            player_pos.x = screen.get_width() - player_size
        if player_pos.y < player_size:
            player_pos.y = player_size
            player_vel.y = 0
        if player_pos.y > screen.get_height() - player_size:
            player_pos.y = screen.get_height() - player_size
            player_vel.y = 0
            on_ground = True
            can_jump = True

    # Quit with Q key
    if keys[pygame.K_q]:
        running = False

    # Update fire animation
    fire_pit.update(dt)

    # Update lightning strikes
    current_time = time.time()
    for i in range(len(lightning_strikes) - 1, -1, -1):
        if not lightning_strikes[i].update(current_time):
            lightning_strikes.pop(i)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(PURPLE)

    # Draw platforms
    for platform in platforms:
        platform.draw()

    # Draw fire pit
    fire_pit.draw()

    # Draw lightning strikes
    for lightning in lightning_strikes:
        lightning.draw()

    # Draw player (unless game over)
    if not game_over:
        # TODO: How do we use a sprite with animation loops here?
        pygame.draw.circle(
            screen, RED, (int(player_pos.x), int(player_pos.y)), player_size
        )

    # Show game over message
    if game_over:
        game_over_text = game_font.render("Ow ow ow fire...", True, RED)
        respawn_text = game_font.render("Respawning...", True, WHITE)
        screen.blit(
            game_over_text,
            (
                screen.get_width() // 2 - game_over_text.get_width() // 2,
                screen.get_height() // 2 - 50,
            ),
        )
        screen.blit(
            respawn_text,
            (
                screen.get_width() // 2 - respawn_text.get_width() // 2,
                screen.get_height() // 2 + 10,
            ),
        )

    # Draw movement counter in top right
    counter_text = counter_font.render(f"Moves: {movement_counter}", True, WHITE)
    screen.blit(counter_text, (screen.get_width() - counter_text.get_width() - 20, 20))

    # flip() the display to put work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
