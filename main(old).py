import pygame
import sys
import math

# init programme
pygame.init()

# Creer une fenetre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Game (SNES Mode 7)")

track = pygame.image.load("assets/track.jpg").convert()
track_width, track_height = track.get_size()

camera_x, camera_y = 400, 400
angle = 0
speed = 0

# clock & fps
clock = pygame.time.Clock()
FPS = 60

def mode7_projection(surface, camera_x, camera_y, angle):
    horizon = HEIGHT // 2
    for screen_y in range(horizon, HEIGHT):
        # Simulate depth: closer rows scale more
        perspective = (screen_y - horizon + 1)
        scale = 240 / perspective  # Focal length; tweak 240 for zoom

        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        for screen_x in range(WIDTH):
            dx = screen_x - WIDTH // 2
            map_x = camera_x + (dx * cos_a - scale * sin_a)
            map_y = camera_y + (dx * sin_a + scale * cos_a)

            # Clamp coordinates
            mx = int(max(0, min(map_x, track_width - 1)))
            my = int(max(0, min(map_y, track_height - 1)))

            color = track.get_at((mx, my))
            surface.set_at((screen_x, screen_y), color)

def draw_horizon():
    screen.fill((100, 200, 255), rect=(0, 0, WIDTH, HEIGHT // 2)) # ciel
    screen.fill((60, 60, 60), rect=(0, HEIGHT // 2, WIDTH, HEIGHT // 2)) # sol

# boucle principale
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    # gestion des evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: speed += 100 + dt
    if keys[pygame.K_DOWN]: speed -= 100 + dt
    if keys[pygame.K_LEFT]: angle -= 2 * dt
    if keys[pygame.K_RIGHT]: angle += 2 * dt

    # camera 
    camera_x += math.cos(angle) * speed * dt
    camera_y += math.sin(angle) * speed * dt

    # draw
    draw_horizon()
    mode7_projection(screen, camera_x, camera_y, angle)

    # screen fill noir, update, max fps
    #screen.fill((0, 0, 0))
    pygame.display.flip()
    #clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()