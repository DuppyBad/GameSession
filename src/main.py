# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
cursor = pygame.mouse.set_cursor(*pygame.cursors.arrow)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)
    player_pos_x_round = round(player_pos[0],0)
    player_pos_y_round = round(player_pos[1],0)
    keys = pygame.key.get_pressed()
    # it checks if it goes out of bounds, there is probably a better way, but oh well.
    if keys[pygame.K_w]:
        if player_pos_y_round < 40:
            player_pos.y += 0
            player_pos.x += 0
        else:
            player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        if player_pos_y_round > 680:
            player_pos.y += 0
            player_pos.x += 0
        else:
            player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        if player_pos_x_round < 43:
            player_pos.y += 0
            player_pos.x += 0
        else:
            player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        if player_pos_x_round > 1238:
            player_pos.y += 0
            player_pos.x += 0
        else:
            player_pos.x += 300 * dt
    if keys[pygame.K_q]:
        pygame.quit()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
