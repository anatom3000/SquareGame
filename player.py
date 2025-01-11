from __future__ import annotations
from typing import Optional
import math

import pygame
import gdicons

from object import Object
from viewport import Viewport, lerp
from rect import Rect

from constants import PLAYER_COLOR, JUMP_VELOCITY, PAD_JUMP_VELOCITY, SHIP_BOOST, HITBOX_WIDTH

gdicons.set_resources_path("./assets/Resources")


def pilImageToSurface(pilImage):
    return pygame.image.frombytes(
        pilImage.tobytes(), pilImage.size, pilImage.mode
    ).convert_alpha()


class AlignAnimation:
    def __init__(self, origin: float, target: float, speed: float):
        self.origin = origin
        self.target = target
        self.duration = abs(target - origin) / speed
        self.t = 0.0

    def tick(self, dt: float):
        self.t += dt
    
    def get(self) -> float:
        return round(lerp(self.origin, self.target, self.t/self.duration) * 10000) // 10000

    def finished(self) -> bool:
        return self.t > self.duration

class Player:
    CUBE_TEXTURE = pilImageToSurface(gdicons.render_icon(
        gamemode="cube",
        id=4,
        primary=11,
        secondary=3,
    ))

    SHIP_TEXTURE = pilImageToSurface(gdicons.render_icon(
        gamemode="ship",
        id=1,
        primary=11,
        secondary=3,
    ))

    def __init__(self, position: (float, float)):
        self.position = position
        self.velocity = (0.0, 0.0)
        self.rotation = 0.0

        self.alignment_anim: Optional[AlignAnimation] = None

        self.on_ground = True
        self.flipped = False
        self.ship = False
        self.check_for_ground_after: Optional[float] = None
        self.recheck_for_ground = False

        self.small_hitbox = (9.0, 9.0)
        self.big_hitbox = (30.0, 30.0)

    def draw(self, viewport: Viewport, show_hitbox: bool):
        if not self.ship:
            self.draw_cube(viewport)
        else:
            self.draw_ship(viewport)

        if show_hitbox:
            viewport.draw_rect(PLAYER_COLOR, self.small_bounding_box, width=HITBOX_WIDTH, widthInPx=True)
            viewport.draw_rect(PLAYER_COLOR, self.big_bounding_box, width=HITBOX_WIDTH, widthInPx=True)

    def draw_cube(self, viewport: Viewport):
        rotation = self.rotation

        viewport.blit_rotated(self.CUBE_TEXTURE, self.big_bounding_box, rotation, False, False)

    def draw_ship(self, viewport: Viewport):
        rotation = self.rotation
        
        cube_rect = Rect((self.position[0]+5.0*math.sin(rotation / 180 * math.pi), self.position[1]+self.sign*5.0*math.cos(rotation / 180 * math.pi)), size=(18.0, 18.0))
        viewport.blit_rotated(self.CUBE_TEXTURE, cube_rect, rotation, False, self.flipped)

        ship_rect = Rect((self.position[0]-4.0*math.sin(rotation / 180 * math.pi), self.position[1]-self.sign*4.0*math.cos(rotation / 180 * math.pi)), size=(37.5, 22.5))
        viewport.blit_rotated(self.SHIP_TEXTURE, ship_rect, rotation, False, self.flipped)

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
            self.alignment_anim = None

            if not self.ship:
                self.rotation += self.sign * dt*(180.0/0.45)
            else:
                self.rotation = -90.0 + math.atan2(self.velocity[0], self.velocity[1]) * 180 / math.pi

        elif self.alignment_anim is not None:
            self.alignment_anim.tick(dt)
            self.rotation = self.alignment_anim.get()

            if self.alignment_anim.finished():
                self.alignment_anim = None
                self.rotation = 90 * round(self.rotation / 90)


    def land(self):
        self.on_ground = True
        target_rotation = 90 * round(self.rotation / 90)

        if self.rotation != target_rotation:
            self.alignment_anim = AlignAnimation(self.rotation, target_rotation, 200)

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

        self.alignment_anim = None

    def yellow_pad_jump(self):
        self.on_ground = False
        self.velocity = (self.velocity[0], self.sign * PAD_JUMP_VELOCITY)
        self.check_for_ground_after = None
