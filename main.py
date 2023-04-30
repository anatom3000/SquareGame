from sys import exit

import pygame
from pygame.locals import *

pygame.init()

RESOLUTION = (1280, 720)
MAX_FPS = 60
BACKGROUND_COLOR = (38, 124, 254)

screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()


running = True

while running:

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)

        if ev.type == KEYUP:
            pass

        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            pass

    screen.fill(BACKGROUND_COLOR)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps())}")

    pygame.display.flip()
    clock.tick(MAX_FPS)
