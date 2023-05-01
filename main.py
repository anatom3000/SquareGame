from sys import exit

import pygame
from pygame.locals import *

import numpy as np

from level import Level
from objects import Object
from viewport import Viewport

from constants import *

pygame.init()


screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
viewport = Viewport(screen, zoom=2.0, position=np.array([200.0, -200.0]))

things = [Object(np.array([15*30.0+30*j, -i*30])) for i in range(4) for j in range(6)]

level = Level(things)

running = True
while running:
    dt = clock.tick(MAX_FPS) / 1000

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)

        if ev.type == KEYUP:
            pass

        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.player_is_holding = True

        if ev.type == MOUSEBUTTONUP:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.player_is_holding = False

    screen.fill(BACKGROUND_COLOR)

    viewport.move(np.array([dt * PLAYER_SPEED * viewport.zoom, 0.0]))
    viewport.tick(dt)

    level.tick(dt)
    level.draw(viewport)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps())}")

    pygame.display.flip()
