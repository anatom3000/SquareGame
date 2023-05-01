from __future__ import annotations

import numpy as np
import pygame

from viewport import Viewport
from constants import *


class Object:
    def __init__(self, position: np.ndarray):
        self.position = position
        self.hitbox = np.array([30, 30])

    def draw(self, viewport: Viewport):
        viewport.draw_rect(OBJECT_COLOR, self.position, self.hitbox, width=0.5)

    @property
    def bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        top_left = self.position - self.hitbox / 2
        bottom_right = self.position + self.hitbox / 2

        return top_left, bottom_right


class Player:
    def __init__(self, position: np.ndarray):
        self.position = position
        self.velocity = np.zeros(2)

        self.on_ground = True

        self.small_hitbox = np.array([15, 15])
        self.big_hitbox = np.array([30, 30])

    def draw(self, viewport: Viewport):
        viewport.draw_rect(PLAYER_COLOR, self.position, self.small_hitbox, width=1)
        viewport.draw_rect(PLAYER_COLOR, self.position, self.big_hitbox, width=1)

    @property
    def small_bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        top_left = self.position - self.small_hitbox / 2
        bottom_right = self.position + self.small_hitbox / 2

        return top_left, bottom_right

    @property
    def big_bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        top_left = self.position - self.big_hitbox / 2
        bottom_right = self.position + self.big_hitbox / 2

        return top_left, bottom_right

    def align_bottom_to_object(self, obj: Object):
        self.position[1] = self.big_hitbox[1] / 2 + obj.position[1] + obj.hitbox[1] / 2

    def jump(self):
        if not self.on_ground:
            return

        self.on_ground = False
        self.velocity[1] = JUMP_VELOCITY
