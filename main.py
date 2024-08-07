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

i = 1

level = Level(
    screen, 
    parse_level(f'assets/Resources/levels/{i}.lvl'),
    'assets/songs/StereoMadness.mp3'
)

paused = False
t = 0
speed = 1.0
done = False

running = True
while running:
    dt = speed * clock.tick(MAX_FPS) / 1000
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
                level.show_hitboxes = not level.show_hitboxes

            if ev.key == K_r:
                level.restart()

            if ev.key == K_SPACE or ev.key == K_UP:
                level.tap()

            if ev.key == K_LEFT:
                i -= 1
                level = Level(
                    screen, 
                    parse_level(f'assets/Resources/levels/{i}.lvl'),
                    'assets/songs/StereoMadness.mp3'
                )

            if ev.key == K_RIGHT:
                i += 1
                level = Level(
                    screen, 
                    parse_level(f'assets/Resources/levels/{i}.lvl'),
                    'assets/songs/StereoMadness.mp3'
                )

            if ev.key == K_f:
                level.player.flipped = not level.player.flipped
                level.player.on_ground = False

            if ev.key == K_t:
                speed /= 2.0
            if ev.key == K_y:
                speed *= 2.0

        if ev.type == KEYDOWN:
            if ev.key == K_SPACE or ev.key == K_UP:
                level.release()

        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.tap()

        if ev.type == MOUSEBUTTONUP:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.release()

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
