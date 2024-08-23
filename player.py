from __future__ import annotations
from typing import Optional
import math

import pygame
import gdicons

from object import Object
from viewport import Viewport
from rect import Rect

from constants import PLAYER_COLOR, JUMP_VELOCITY, PAD_JUMP_VELOCITY, SHIP_BOOST

gdicons.set_resources_path("./assets/Resources")


def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode
    ).convert_alpha()


class Player:
    def __init__(self, position: (float, float)):
        self.position = position
        self.velocity = (0.0, 0.0)
        self.rotation = 0.0

        self.texture = pilImageToSurface(gdicons.render_icon(
            gamemode="cube",
            id=4,
            primary=11,
            secondary=3,
        ))

        self.on_ground = True
        self.flipped = False
        self.ship = False
        self.check_for_ground_after: Optional[float] = None
        self.recheck_for_ground = False
        
        self.small_hitbox = (9.0, 9.0)
        self.big_hitbox = (30.0, 30.0)

    def draw(self, viewport: Viewport, show_hitbox: bool):
        if self.ship:
            rotation = math.atan2(self.velocity[0], self.velocity[1]) * 180 / math.pi
        else:
            rotation = self.rotation

        viewport.blit_rotated(self.texture, self.big_bounding_box, rotation, False, False)
        if show_hitbox:
            viewport.draw_rect(PLAYER_COLOR, self.small_bounding_box, width=1.5)
            viewport.draw_rect(PLAYER_COLOR, self.big_bounding_box, width=1.5)

    @property
    def small_bounding_box(self) -> Rect:
        return Rect(self.position, self.small_hitbox)

    @property
    def big_bounding_box(self) -> Rect:
        return Rect(self.position, self.big_hitbox)

    @property
    def sign(self):
        return -1 if self.flipped else 1

    def align_to_object(self, obj: Object):
        self.position = (
            self.position[0],
            obj.position[1] + self.sign * self.big_hitbox[1] / 2 + self.sign * obj.kind.hitbox[1] / 2,
        )
        self.check_for_ground_after = obj.position[0] + obj.kind.hitbox[0] / 2 + self.big_hitbox[0] / 2

    def rotate(self, dt: float):
        self.rotation %= 360.0

        if not self.on_ground:
            self.rotation += self.sign * dt*(180.0/0.45)

    def land(self):
        self.on_ground = True
        self.rotation = 90 * round(self.rotation / 90)

    def jump(self, dt: float):
        if not self.ship:
            if not self.on_ground:
                return

            self.velocity = (
                self.velocity[0],
                self.sign * JUMP_VELOCITY,
            )
            self.on_ground = False
            self.check_for_ground_after = None
        else:
            self.velocity = (
                self.velocity[0],
                self.velocity[1] + self.sign * SHIP_BOOST * dt,
            )
            self.on_ground = False
            self.check_for_ground_after = None

    def yellow_pad_jump(self):
        self.on_ground = False
        self.velocity = (self.velocity[0], self.sign * PAD_JUMP_VELOCITY)
        self.check_for_ground_after = None

