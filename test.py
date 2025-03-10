import pygame

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

# Player setup
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_vel = pygame.Vector2(0, 0)
player_size = 40
on_ground = False
can_jump = False  # To prevent multi-jumping


# Platform class
class Platform:
    def __init__(self, x, y, width, height, color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


# Create platforms
platforms = [
    Platform(0, 650, 1280, 70),  # Ground
    Platform(200, 550, 300, 20),
    Platform(600, 450, 300, 20),
    Platform(300, 350, 200, 20),
    Platform(700, 250, 300, 20),
    Platform(100, 150, 200, 20),
]

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and can_jump:
                player_vel.y = JUMP_POWER
                can_jump = False  # After jumping, cannot immediately jump

    # Get pressed keys
    keys = pygame.key.get_pressed()

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

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(PURPLE)

    # Draw platforms
    for platform in platforms:
        platform.draw()

    # Draw player
    pygame.draw.circle(screen, RED, (int(player_pos.x), int(player_pos.y)), player_size)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
