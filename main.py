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


things = []
for i in range(5):
    things.append(Object(np.array([6.5*30+5*30*i, 30*i])))

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
                level.input_activated = True

        if ev.type == MOUSEBUTTONUP:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.input_activated = False

    screen.fill(BACKGROUND_COLOR)

    if not level.stopped:
        viewport.move(np.array([dt * PLAYER_SPEED * viewport.zoom, 0.0]))

    viewport.tick(dt)

    for _ in range(PHYSICS_SUBTICKS):
        level.tick(dt/PHYSICS_SUBTICKS)

    level.draw(viewport)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps())} - {level.input_activated}")

    pygame.display.flip()
