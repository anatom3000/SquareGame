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


viewport = Viewport(screen, zoom=2.0, position=np.array([200.0, GROUND_HEIGHT-30*15]))

spacing = (4, 1)

things = []
for i in range(100):
    things.append(Object(np.array([6.5*30+spacing[0]*30*i, 135+spacing[1]*30*i])))
    # things.append(Object(np.array([4.5*30+30*i, 135])))
    # things.append(Object(np.array([30*i, 75])))

# things.append(Object(np.array([4.5*30, 60])))
# things.append(Object(np.array([45.0, 124.5])))
# things.append(Object(np.array([60+75.0, 124.75])))
# things.append(Object(np.array([60+105.0, 124.5])))

level = Level(things)

paused = False
t = 0

running = True
while running:
    dt = clock.tick(MAX_FPS) / 1000 * 1.0
    pygame.key.set_repeat(50, 20)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)

        if ev.type == KEYUP:
            if ev.key == K_RETURN:
                paused = not paused

            if ev.key == K_RIGHT:
                t += dt
                if not level.stopped:
                    viewport.move(np.array([dt * PLAYER_SPEED * viewport.zoom, 0.0]))

                viewport.tick(dt)

                for _ in range(PHYSICS_SUBTICKS):
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
        t += dt
        if not level.stopped:
            viewport.move(np.array([dt * PLAYER_SPEED * viewport.zoom, 0.0]))

        viewport.tick(dt)

        for _ in range(PHYSICS_SUBTICKS):
            level.tick(dt / PHYSICS_SUBTICKS)

    level.draw(viewport)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps())} - {level.player.position} - t = {round(t, 2)}")

    pygame.display.flip()
