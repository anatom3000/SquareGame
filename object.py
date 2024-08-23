from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from enum import Enum

import pygame

from viewport import Viewport
from rect import Rect


class HitboxKind(Enum):
    SOLID = 1
    HAZARD = 2
    DECORATION = 3
    YELLOW_ORB = 4
    YELLOW_PAD = 5
    BLUE_PORTAL = 6
    YELLOW_PORTAL = 7


@dataclass
class ObjectKind:
    texture_path: pygame.Surface
    hitbox_kind: HitboxKind
    texture_size: Optional[(float, float)] = None
    hitbox: Optional[(float, float)] = None

    def new(self, **kwargs):
        return Object(kind=self, **kwargs)

    def __post_init__(self):
        self.texture = pygame.image.load(self.texture_path).convert_alpha()


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

    def draw(self, viewport: Viewport, show_hitbox: bool):
        viewport.blit_rotated(self.kind.texture, self.display_box, self.rotation, self.hflip, self.vflip)

        if show_hitbox:
            if self.kind.hitbox_kind == HitboxKind.SOLID:
                color = (0, 0, 255)
            elif self.kind.hitbox_kind == HitboxKind.HAZARD:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)

            viewport.draw_rect(color, self.bounding_box, width=1.5)


object_kinds = {
    1: ObjectKind( # default block
        "assets/default_block.png",
        HitboxKind.SOLID,
    ),
    2: ObjectKind( # flat deco block
        "assets/flat_deco_block.png",
        HitboxKind.SOLID,
    ),
    3: ObjectKind( # outer corner deco block
        "assets/outer_corner_deco_block.png",
        HitboxKind.SOLID,
    ),
    4: ObjectKind( # inner corner deco block
        "assets/inner_corner_deco_block.png",
        HitboxKind.SOLID,
    ),
    5: ObjectKind( # inner deco block
        "assets/inner_deco_block.png",
        HitboxKind.DECORATION,
        (30, 30),
    ),
    6: ObjectKind( # pipe end deco block
        "assets/pipe_end_deco_block.png",
        HitboxKind.SOLID,
    ),
    7: ObjectKind( # pipe deco block
        "assets/pipe_deco_block.png",
        HitboxKind.SOLID,
    ),
    8: ObjectKind( # default spike
        "assets/default_spike.png",
        HitboxKind.HAZARD,
        (30, 30),
    ),
    9: ObjectKind( # ground spike
        "assets/ground_spike.png",
        HitboxKind.HAZARD,
        (30, 27),
    ),
    10: ObjectKind( # blue portal
        "assets/default_block.png",
        HitboxKind.BLUE_PORTAL,
    ),
    11: ObjectKind( # yellow portal
        "assets/default_block.png",
        HitboxKind.YELLOW_PORTAL,
    ),
    35: ObjectKind(
        "assets/yellow_pad.png",
        HitboxKind.YELLOW_PAD,
    ),
    36: ObjectKind( # yellow orb
        "assets/yellow_orb.png",
        HitboxKind.YELLOW_ORB,
        (30, 30),
    ),
    39: ObjectKind( # little spike
        "assets/little_spike.png",
        HitboxKind.HAZARD,
        (30, 14),
    ),
    40: ObjectKind( # default slab
        "assets/default_slab.png",
        HitboxKind.SOLID,
    ),
}

with open("assets/hitboxes.json") as f:
    import json
    hitboxes = json.load(f)
    for id in object_kinds.keys():
        if object_kinds[id].hitbox is not None:
            continue

        box = hitboxes.get(str(id))
        if box is None:
            object_kinds[id].hitbox = (0.0, 0.0)
            continue

        object_kinds[id].hitbox = (box["w"], box["h"])
        if object_kinds[id].texture_size is None:
            object_kinds[id].texture_size = object_kinds[id].hitbox

