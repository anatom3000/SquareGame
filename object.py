from __future__ import annotations

import pygame

from viewport import Viewport
from rect import Rect

from constants import *


class Object:
    def __init__(self, position: np.ndarray):
        self.position = position
        self.hitbox = np.array([30.0, 30.0])

    def draw(self, viewport: Viewport):
        viewport.draw_rect(OBJECT_COLOR, self.bounding_box, width=0.5)

    @property
    def bounding_box(self) -> Rect:
        return Rect(self.position, self.hitbox)


