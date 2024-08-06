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
