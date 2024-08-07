from __future__ import annotations

import numpy as np
import pygame.mixer

from object import Object, HitboxKind
from player import Player
from rect import Rect
from constants import PLAYER_SPEED, GROUND_HEIGHT, CAMERA_TRIGGER_UP_ZONE, CAMERA_TRIGGER_DOWN_ZONE, CAMERA_MOVE_DISTANCE, PLAYER_GRAVITY, SOLID_ALIGNMENT_TOLERANCE_ON_GROUND, SOLID_ALIGNMENT_TOLERANCE, RESTART_DELAY
from viewport import Viewport


class Level:
    def __init__(self, screen, objects: list[Object], song: str):
        self.screen = screen
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        pygame.mixer.music.pause()
        self.all_objects = sorted(objects, key=lambda x: x.position[0])
        self.restart()

        self.noclip = False
        self.show_hitboxes = False

    def restart(self):
        pygame.mixer.music.rewind()

        self.viewport = Viewport(self.screen, zoom=9 / 4, position=np.array([200.0, GROUND_HEIGHT - 30 * 15]))
        self.player = Player(position=np.array([0.0, 105]))
        self.objects = self.all_objects.copy()

        self.stop_time = None
        self.input_activated = False
        self.input_orb_activated = False
        self.first_right_invisible_object = None

        for obj in self.objects:
            if obj.kind.hitbox_kind in (HitboxKind.YELLOW_ORB, HitboxKind.YELLOW_PAD):
                obj.activated = False

    def tap(self):
        self.input_activated = True
        self.input_orb_activated = True

    def release(self):
        self.input_activated = False
        self.input_orb_activated = False

    def tick(self, dt: float):
        if self.stop_time is not None:
            if self.stop_time >= RESTART_DELAY:
                self.stop_time = None
                self.restart()
            else:
                self.stop_time += dt
            return

        self.tick_camera(dt)

        self.player.velocity[0] = PLAYER_SPEED

        if not self.player.on_ground:
            self.player.velocity[1] -= self.player.sign * PLAYER_GRAVITY * dt

        if self.input_activated:
            self.player.jump()

        self.player.rotate(dt)

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
        elif self.player.sign * self.player.velocity[1] < 0.0:
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
            
            match obj.kind.hitbox_kind:

                case HitboxKind.SOLID:
                    self.handle_solid(obj, alignment_tolerance, big_player_box, small_player_box)
                case HitboxKind.HAZARD:
                    self.handle_hazard(obj, big_player_box)
                case HitboxKind.DECORATION:
                    pass  # nothing to do
                case HitboxKind.YELLOW_ORB:
                    self.handle_yellow_orb(obj)
                case HitboxKind.YELLOW_PAD:
                    self.handle_yellow_pad(obj)
                case HitboxKind.BLUE_PORTAL:
                    self.handle_gravity_portal(obj, flipped=False)
                case HitboxKind.YELLOW_PORTAL:
                    self.handle_gravity_portal(obj, flipped=True)
                    pass
                case other:
                    raise RuntimeError(f"unreachable: unknown object kind {other}")

        if last_left_invisible_object is not None:
            self.objects = self.objects[last_left_invisible_object + 1:]
            if self.first_right_invisible_object is not None:
                self.first_right_invisible_object -= last_left_invisible_object

        self.player.position += self.player.velocity * dt

        if self.player.position[1] < GROUND_HEIGHT + self.player.big_hitbox[1] / 2:
            self.player.position[1] = GROUND_HEIGHT + self.player.big_hitbox[1] / 2
            if not self.player.flipped:
                self.player.land()

    def handle_solid(self, obj: Object, alignment_tolerance: float, big_player_box: Rect, small_player_box: Rect):
        obj_box = obj.bounding_box

        if big_player_box.collide_rect(obj_box):
            if self.player.flipped:
                distance_to_top = obj_box.bottom - big_player_box.top
            else:
                distance_to_top = big_player_box.bottom - obj_box.top

            if distance_to_top > alignment_tolerance and not self.player.on_ground:
                self.player.align_to_object(obj)
                self.player.land()
                if self.input_activated:
                    self.player.jump()
                else:
                    self.player.velocity[1] = 0.0

            if small_player_box.collide_rect(obj_box):
                self.stop()

    def handle_hazard(self, obj: Object, big_player_box: Rect):
        if big_player_box.collide_rect(obj.bounding_box):
            self.stop()

    def handle_yellow_orb(self, obj: Object):
        if not self.player.big_bounding_box.collide_rect(obj.bounding_box):
            return

        if obj.activated:
            return

        if not (self.input_activated and self.input_orb_activated):
            return

        obj.activated = True
        self.input_orb_activated = False
        self.player.on_ground = True
        self.player.jump()

    def handle_yellow_pad(self, obj: Object):
        if not self.player.big_bounding_box.collide_rect(obj.bounding_box):
            return

        if obj.activated:
            return

        obj.activated = True
        self.player.yellow_pad_jump()

    def handle_gravity_portal(self, obj: Object, flipped: bool):
        if not self.player.big_bounding_box.collide_rect(obj.bounding_box):
            return

        self.player.flipped = flipped
        self.player.on_ground = False

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

    def draw(self):
        for obj in self.objects[:self.first_right_invisible_object]:
            obj.draw(self.viewport, self.show_hitboxes)

        self.player.draw(self.viewport, self.show_hitboxes)

    def stop(self):
        if not self.noclip:
            self.stop_time = 0.0
            pygame.mixer.music.pause()
