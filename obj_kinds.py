import numpy as np
import pygame

from object import ObjectKind, HitboxKind

obj_kinds = {
    1: ObjectKind(
        pygame.image.load('assets/default_block.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.SOLID,
        np.array([30, 30])
    ),
    8: ObjectKind(
        pygame.image.load('assets/default_spike.png').convert_alpha(),
        np.array([30, 30]),
        HitboxKind.HAZARD,
        np.array([6, 12])
    ),
}
