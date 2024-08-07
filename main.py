from sys import exit

import pygame
from pygame.locals import *

import numpy as np

from constants import RESOLUTION, MAX_FPS, BACKGROUND_COLOR, PHYSICS_SUBTICKS

pygame.init()

screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)

from level import Level
from viewport import Viewport
from rect import Rect


from level_parser import parse_level

clock = pygame.time.Clock()

level = Level(screen, parse_level('assets/Resources/levels/test.lvl'))
pygame.mixer.music.load('assets/songs/StereoMadness.mp3')
pygame.mixer.music.play()
pygame.mixer.music.pause()


paused = False
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
            if ev.key == K_ESCAPE:
                paused = not paused

            if ev.key == K_RIGHT:
                level.tick(dt / PHYSICS_SUBTICKS)

            if ev.key == K_n:
                level.noclip = not level.noclip

            if ev.key == K_h:
                level.player.render_hitbox = not level.player.render_hitbox

            if ev.key == K_r:
                level.restart()
            # 1 = left click; 2 = middle click; 

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
        if (level.stop_time is None) and (not pygame.mixer.music.get_busy()):
            pygame.mixer.music.unpause()

        for _ in range(PHYSICS_SUBTICKS):
            level.tick(dt / PHYSICS_SUBTICKS)
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    level.draw()

    # if not done and t > 2.0:
    #     level.viewport.target_position += 100.0
    #     done = True

    pygame.display.set_caption(f"FPS: {round(clock.get_fps())}")

    pygame.display.flip()
