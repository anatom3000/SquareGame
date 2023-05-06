from sys import exit

import pygame
from pygame.locals import *

import numpy as np

from level import Level
from object import Object
from viewport import Viewport
from rect import Rect

from constants import *

pygame.init()

screen = pygame.display.set_mode(RESOLUTION)

clock = pygame.time.Clock()

viewport = Viewport(screen, zoom=2.0, position=np.array([200.0, GROUND_HEIGHT - 30 * 15]))

spacing = (4, 1)
first_block = (5, 0)

things = []
for i in range(100):
    things.append(
        Object(np.array([first_block[0] * 30 + spacing[0] * 30 * i, 105 + first_block[1] * 30 + spacing[1] * 30 * i])))
    # things.append(Object(np.array([4.5*30+30*i, 135])))
    # things.append(Object(np.array([30*i, 75])))

# things.append(Object(np.array([4.5*30, 60])))
# things.append(Object(np.array([45.0, 124.5])))
# things.append(Object(np.array([60+75.0, 124.75])))
# things.append(Object(np.array([60+105.0, 124.5])))

level = Level(viewport, things)

paused = True
t = 0
done = False

running = True
while running:
    dt = clock.tick(MAX_FPS) / 1000
    t += dt

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)

        if ev.type == KEYUP:
            if ev.key == K_RETURN:
                paused = not paused

            if ev.key == K_RIGHT:
                level.tick(dt / PHYSICS_SUBTICKS)

        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.input_activated = True

        if ev.type == MOUSEBUTTONUP:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.input_activated = False

    screen.fill(BACKGROUND_COLOR)

    if not paused:
        for _ in range(PHYSICS_SUBTICKS):
            level.tick(dt / PHYSICS_SUBTICKS)
    else:
        level.viewport.tick(dt)

    level.draw(viewport)

    if not done and t > 2.0:
        level.viewport.move(np.array([100, 100]))
        done = True

    pygame.display.set_caption(f"FPS: {round(clock.get_fps())} - {pygame.mouse.get_pos()} - t = {round(t, 2)}")

    pygame.display.flip()
