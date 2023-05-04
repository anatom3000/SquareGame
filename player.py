from __future__ import annotations

import numpy as np
import pygame

from objects import Object
from viewport import Viewport
from rect import Rect

from constants import *

class Player:
    def __init__(self, position: np.ndarray):
        self.position = position
        self.velocity = np.zeros(2, dtype=float)

        self.on_ground = True
        self.check_for_ground_after: Optional[float] = None
        self.recheck_for_ground = False

        self.small_hitbox = np.array([9.0, 9.0])
        self.big_hitbox = np.array([30.0, 30.0])

    def draw(self, viewport: Viewport):
        viewport.draw_rect(PLAYER_COLOR, self.small_bounding_box, width=1.5)
        viewport.draw_rect(PLAYER_COLOR, self.big_bounding_box, width=1.5)

    @property
    def small_bounding_box(self) -> Rect:
        return Rect(self.position, self.small_hitbox)

    @property
    def big_bounding_box(self) -> Rect:
        return Rect(self.position, self.big_hitbox)

    def align_to_object(self, obj: Object):
        self.position[1] = self.big_hitbox[1] / 2 + obj.position[1] + obj.hitbox[1] / 2
        self.check_for_ground_after = obj.position[0] + obj.hitbox[0] / 2 + self.big_hitbox[0] / 2

    def jump(self):
        if not self.on_ground:
            return

        self.on_ground = False
        self.velocity[1] = JUMP_VELOCITY

        self.check_for_ground_after = None
