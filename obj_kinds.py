import numpy as np
import pygame

from object import ObjectKind, HitboxKind

default_block = ObjectKind(
    pygame.image.load('assets/default_block.png').convert_alpha(),
    np.array([30, 30]),
    HitboxKind.SOLID,
    np.array([30, 30])
)

obj_kinds = {
    1: default_block,
    # TODO: add all block variations
    2: default_block,
    3: default_block,
    4: default_block,
    5: default_block,
    6: default_block,
    7: default_block,
    40: default_block,
    8: ObjectKind(
        pygame.image.load('assets/default_spike.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.HAZARD,
        np.array([6, 12])
    ),
    39: ObjectKind(
        pygame.image.load('assets/little_spike.png').convert_alpha(),
        np.array([30, 14]),
        HitboxKind.HAZARD,
        np.array([6, 5.6])
    ),
}
