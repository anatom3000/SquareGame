from __future__ import annotations

import numpy as np
import pygame.mixer

from object import Object, HitboxKind
from player import Player
from constants import *
from viewport import Viewport


class Level:
    def __init__(self, viewport: Viewport, objects: list[Object]):
        self.viewport = viewport

        self.player = Player(position=np.array([0.0, 105]))
        self.objects = sorted(objects, key=lambda x: x.position[0])

        self.input_activated = False
        self.stopped = False

        self.first_right_invisible_object = None

    def tick(self, dt: float):
        if self.stopped:
            return

        self.tick_camera(dt)

        self.player.velocity[0] = PLAYER_SPEED

        if not self.player.on_ground:
            self.player.velocity[1] -= PLAYER_GRAVITY * dt

        if self.input_activated:
            self.player.jump()

        self.player.recheck_for_ground = False
        if self.player.check_for_ground_after is not None:
            if self.player.position[0] >= self.player.check_for_ground_after:
                self.player.on_ground = False
                self.player.recheck_for_ground = True
                self.player.check_for_ground_after = None

        small_player_box = self.player.small_bounding_box
        big_player_box = self.player.big_bounding_box

        if self.player.recheck_for_ground:
            alignment_tolerance = -SOLID_ALIGNMENT_TOLERANCE_ON_GROUND
        elif self.player.velocity[1] < 0.0:
            alignment_tolerance = -SOLID_ALIGNMENT_TOLERANCE
        else:
            alignment_tolerance = 0.0

        camera_left = self.viewport.left
        camera_right = self.viewport.right

        last_left_invisible_object = None

        for i, obj in enumerate(self.objects):
            if camera_left > obj.bounding_box.right:
                last_left_invisible_object = i
                continue

            if camera_right < obj.bounding_box.left:
                first_right_invisible_object = i
                break  # objects are sorted by x position

            if obj.kind.hitbox_kind == HitboxKind.SOLID:
                self.handle_solid(obj, alignment_tolerance, big_player_box, small_player_box)
            elif obj.kind.hitbox_kind == HitboxKind.HAZARD:
                self.handle_hazard(obj, big_player_box)
            elif obj.kind.hitbox_kind == HitboxKind.DECORATION:
                pass  # nothing to do
            else:
                raise RuntimeError("unreachable: unknown object kind")

        if last_left_invisible_object is not None:
            self.objects = self.objects[last_left_invisible_object + 1:]
            if self.first_right_invisible_object is not None:
                self.first_right_invisible_object -= last_left_invisible_object

        self.player.position += self.player.velocity * dt

        if self.player.position[1] < GROUND_HEIGHT + self.player.big_hitbox[1] / 2:
            self.player.position[1] = GROUND_HEIGHT + self.player.big_hitbox[1] / 2
            self.player.on_ground = True

    def handle_solid(self, obj: Object, alignment_tolerance: float, big_player_box: Rect, small_player_box: Rect):
        obj_box = obj.bounding_box

        if big_player_box.collide_rect(obj_box):
            distance_to_top = big_player_box.bottom - obj_box.top
            if distance_to_top > alignment_tolerance:
                self.player.align_to_object(obj)
                self.player.on_ground = True
                if self.input_activated:
                    self.player.jump()
                else:
                    self.player.velocity[1] = 0.0

            if small_player_box.collide_rect(obj_box):
                self.stop()

    def handle_hazard(self, obj: Object, big_player_box: Rect):
        if big_player_box.collide_rect(obj.bounding_box):
            self.stop()

    def tick_camera(self, dt: float):
        # self.viewport.move(np.array([dt * PLAYER_SPEED * self.viewport.zoom, 0.0]))
        self.viewport.position[0] += dt * PLAYER_SPEED * self.viewport.zoom
        self.viewport.target_position[0] += dt * PLAYER_SPEED * self.viewport.zoom

        player_distance_to_screen_top = self.viewport.target_top - self.player.position[1]
        if player_distance_to_screen_top < CAMERA_TRIGGER_UP_ZONE:
            self.viewport.target_position[1] -= (CAMERA_TRIGGER_UP_ZONE + CAMERA_MOVE_DISTANCE)

        player_distance_to_screen_bottom = self.player.position[1] - self.viewport.target_bottom

        if player_distance_to_screen_bottom < CAMERA_TRIGGER_DOWN_ZONE:
            self.viewport.target_position[1] += (CAMERA_TRIGGER_DOWN_ZONE + CAMERA_MOVE_DISTANCE)

        self.viewport.tick(dt)

    def draw(self, viewport: Viewport):
        for obj in self.objects[:self.first_right_invisible_object]:
            obj.draw(viewport)

        self.player.draw(viewport)

    def stop(self):
        self.stopped = True
        pygame.mixer.music.stop()
