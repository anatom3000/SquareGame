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

        self.solid_hitbox = np.array([15, 15])
        self.hasard_hitbox = np.array([30, 30])

    def draw(self, viewport: Viewport):
        viewport.draw_rect(PLAYER_COLOR, self.position, self.solid_hitbox, width=0.5)
        viewport.draw_rect(PLAYER_COLOR, self.position, self.hasard_hitbox, width=0.5)

    @property
    def solid_bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        top_left = self.position - self.solid_hitbox / 2
        bottom_right = self.position + self.solid_hitbox / 2

        return top_left, bottom_right

    @property
    def hasard_bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        top_left = self.position - self.hasard_hitbox / 2
        bottom_right = self.position + self.hasard_hitbox / 2

        return top_left, bottom_right
