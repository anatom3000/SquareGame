from __future__ import annotations

import numpy as np
import pygame
from pygame import Rect

from viewport import Viewport
from constants import *


class Object:
    def __init__(self, position: np.ndarray):
        self.position = position
        self.hitbox = np.array([30.0, 30.0])

    def draw(self, viewport: Viewport):
        viewport.draw_rect(OBJECT_COLOR, self.position, self.hitbox, width=0.5)

    @property
    def bounding_box(self) -> Rect:
        rect = pygame.Rect((0, 0, 0, 0))

        rect.size = self.hitbox
        rect.center = self.position

        return rect


class Player:
    def __init__(self, position: np.ndarray):
        self.position = position
        self.velocity = np.zeros(2, dtype=float)

        self.on_ground = True
        self.check_for_ground_after: Optional[float] = None

        self.small_hitbox = np.array([15.0, 15.0])
        self.big_hitbox = np.array([30.0, 30.0])

    def draw(self, viewport: Viewport):
        viewport.draw_rect(PLAYER_COLOR, self.position, self.small_hitbox, width=1)
        viewport.draw_rect(PLAYER_COLOR, self.position, self.big_hitbox, width=1)

    @property
    def small_bounding_box(self) -> Rect:
        rect = pygame.Rect((0, 0, 0, 0))

        rect.size = self.small_hitbox
        rect.center = self.position

        return rect

    @property
    def big_bounding_box(self) -> Rect:
        rect = pygame.Rect((0, 0, 0, 0))

        rect.size = self.big_hitbox
        rect.center = self.position

        return rect

    def align_to_object(self, obj: Object):
        self.position[1] = self.big_hitbox[1] / 2 + obj.position[1] + obj.hitbox[1] / 2
        self.check_for_ground_after = obj.position[0] + obj.hitbox[0] / 2 + self.big_hitbox[0] / 2

    def jump(self):
        if not self.on_ground:
            return

        self.on_ground = False
        self.velocity[1] = JUMP_VELOCITY
