from sys import exit

import pygame
from pygame.locals import *

import numpy as np

from level import Level
from object import Object, ObjectKind, HitboxKind
from viewport import Viewport
from rect import Rect

from constants import *

pygame.init()

screen = pygame.display.set_mode(RESOLUTION)

from obj_kinds import obj_kinds


clock = pygame.time.Clock()

viewport = Viewport(screen, zoom=9/4, position=np.array([200.0, GROUND_HEIGHT - 30 * 15]))


def level_helper(kind: ObjectKind, spacing: (int, int), start: (int, int), n: (int, int)):
    objects = []
    for i in range(n):
        objects.append(kind.new(np.array([15 + start[0] * 30 + spacing[0] * 30 * i, 105 + start[1] * 30 + spacing[1] * 30 * i])))

    return objects

things = level_helper(obj_kinds[1], (4, 1), (5, 0), 4)
things += level_helper(obj_kinds[1], (1, -0.25), (18, 3), 32)

level = Level(viewport, things)

paused = True
t = 0
done = False

running = True
while running:
    dt = clock.tick(MAX_FPS) / 1000 * 0.25
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

    level.draw(viewport)

    # if not done and t > 2.0:
    #     level.viewport.target_position += 100.0
    #     done = True

    mouse_pos = viewport.convert_position_from_screen(np.array(pygame.mouse.get_pos()))

    pygame.display.set_caption(f"FPS: {round(clock.get_fps())} - {np.round(mouse_pos, 2)} - t = {np.round(level.player.position, 2)}")

    pygame.display.flip()
