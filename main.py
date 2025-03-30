from sys import exit, argv

import pygame
from pygame.locals import *

from constants import RESOLUTION, MAX_FPS, BACKGROUND_COLOR, PHYSICS_SUBTICKS

pygame.init()

screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)

from level import Level
from viewport import Viewport
from rect import Rect
from level_parser import parse_level, parse_level_string

clock = pygame.time.Clock()

i = 1
if len(argv) > 1:
    level_id = int(argv[1])

    import requests

    headers = {
        "User-Agent": ""
    }

    data = {
        "levelID": level_id,
        "secret": "Wmfd2893gb7"
    }

    url = "http://www.boomlings.com/database/downloadGJLevel22.php"

    req = requests.post(url=url, data=data, headers=headers).text.split(':')[1::2]

    if req == []:
        print("invalid level id")
        exit(42)

    level_data = parse_level_string(req[3])
else:
    level_data = parse_level(f'assets/Resources/levels/{i}.lvl')


level = Level(
    screen, 
    level_data,
    'assets/songs/StereoMadness.mp3'
)

paused = False
t = 0
speed = 1
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
                level.release()

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

            if ev.key == K_s:
                level.player.ship = not level.player.ship

            if ev.key == K_t:
                speed /= 2.0
            if ev.key == K_y:
                speed *= 2.0

        if ev.type == KEYDOWN:
            if ev.key == K_SPACE or ev.key == K_UP:
                level.tap()

        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.tap()

        if ev.type == MOUSEBUTTONUP:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                level.release()

        if ev.type == WINDOWRESIZED or ev.type == WINDOWSIZECHANGED:
            factor = ev.y / level.viewport.resolution[1]
            level.viewport.resolution = (ev.x, ev.y)

            level.viewport.zoom *= factor
            level.viewport.position = (factor*level.viewport.position[0], factor*level.viewport.position[1])

            level.viewport.target_zoom *= factor
            level.viewport.target_position = (factor*level.viewport.target_position[0], factor*level.viewport.target_position[1])

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
