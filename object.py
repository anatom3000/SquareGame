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

    def new(self, **kwargs):
        return Object(kind=self, **kwargs)

import functools


@functools.cache
def rotate_texture(texture, angle, hflip, vflip):
    texture = pygame.transform.flip(texture, hflip, vflip)
    texture = pygame.transform.rotate(texture, -angle)

    return texture


@dataclass
class Object:
    kind: ObjectKind
    position: np.ndarray
    hflip: bool
    vflip: bool
    rotation: float

    def __post_init__(self):
        self.bounding_box = Rect(self.position, self.kind.hitbox)
        self.display_box = Rect(self.position, self.kind.texture_size)

    def draw(self, viewport: Viewport):
        rotated = rotate_texture(self.kind.texture, self.rotation, self.hflip, self.vflip)

        viewport.blit(rotated, self.display_box)
        # viewport.draw_rect(OBJECT_COLOR, self.bounding_box, width=0.5)


