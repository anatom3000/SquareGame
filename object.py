from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
import pygame

from viewport import Viewport
from rect import Rect


class HitboxKind(Enum):
    SOLID = 1
    HAZARD = 2
    DECORATION = 3
    SPECIAL = 4


@dataclass
class ObjectKind:
    texture: pygame.Surface
    texture_size: np.ndarray
    hitbox_kind: HitboxKind
    hitbox: np.ndarray

    def new(self, **kwargs):
        return Object(kind=self, **kwargs)


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
        viewport.blit_rotated(self.kind.texture, self.display_box, self.rotation, self.hflip, self.vflip)
        # viewport.draw_rect(OBJECT_COLOR, self.bounding_box, width=0.5)


object_kinds = {
    1: ObjectKind(
        pygame.image.load('assets/default_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.SOLID,
        np.array([30, 30])
    ),

    2: ObjectKind( # flat deco block
        pygame.image.load('assets/flat_deco_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.SOLID,
        np.array([30, 30])
    ),

    3: ObjectKind( # outer corner deco block
        pygame.image.load('assets/outer_corner_deco_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.SOLID,
        np.array([30, 30])
    ),
    4: ObjectKind( # inner corner deco block
        pygame.image.load('assets/inner_corner_deco_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.SOLID,
        np.array([30, 30])
    ),
    5: ObjectKind( # inner deco block
        pygame.image.load('assets/inner_deco_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.DECORATION,
        np.array([30, 30])
    ),
    6: ObjectKind( # pipe end deco block
        pygame.image.load('assets/pipe_end_deco_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.SOLID,
        np.array([30, 30])
    ),
    7: ObjectKind( # pipe deco block
        pygame.image.load('assets/pipe_deco_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.SOLID,
        np.array([30, 30])
    ),

    40: ObjectKind( # default slab
        pygame.image.load('assets/default_slab.png').convert_alpha(),
        np.array([30, 14]),
        HitboxKind.SOLID,
        np.array([30, 14])
    ),

    8: ObjectKind( # default spike
        pygame.image.load('assets/default_spike.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.HAZARD,
        np.array([6, 12])
    ),
    39: ObjectKind( # little spike
        pygame.image.load('assets/little_spike.png').convert_alpha(),
        np.array([30, 14]),
        HitboxKind.HAZARD,
        np.array([6, 5.6])
    ),

    9: ObjectKind( # ground spike
        pygame.image.load('assets/ground_spike.png').convert_alpha(),
        np.array([30, 27]),
        HitboxKind.HAZARD,
        np.array([9.0, 10.8]),
    )
}
