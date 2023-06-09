from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
import pygame

from viewport import Viewport
from rect import Rect

from constants import *


class HitboxKind(Enum):
    SOLID = 1
    HAZARD = 2
    DECORATION = 3


@dataclass
class ObjectKind:
    texture: pygame.Surface
    texture_size: np.ndarray
    hitbox_kind: HitboxKind
    hitbox: np.ndarray

    def new(self, position: np.ndarray):
        return Object(self, position)


class Object:
    def __init__(self, kind: ObjectKind, position: np.ndarray):
        self.position = position
        self.kind = kind

        self.bounding_box = Rect(self.position, self.kind.hitbox)
        self.display_box = Rect(self.position, self.kind.texture_size)

    def draw(self, viewport: Viewport):
        viewport.blit(self.kind.texture, self.display_box)
        # viewport.draw_rect(OBJECT_COLOR, self.bounding_box, width=0.5)


