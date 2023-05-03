from __future__ import annotations

import numpy as np


class Rect:
    def __init__(self, center: np.ndarray, size: np.ndarray):
        self.center = np.array(center, dtype=float)
        self.size = np.array(size, dtype=float)

        self.top = self.center[1] + self.size[1] / 2
        self.bottom = self.center[1] - self.size[1] / 2

        self.left = self.center[0] - self.size[0] / 2
        self.right = self.center[0] + self.size[0] / 2

    def collide_rect(self, other: Rect) -> bool:
        return self.left <= other.right \
            and self.right >= other.left \
            and self.top >= other.bottom \
            and self.bottom <= other.top

    @property
    def topleft(self):
        return np.array((self.left, self.top))

    @property
    def topright(self):
        return np.array((self.right, self.top))

    @property
    def bottomleft(self):
        return np.array((self.left, self.bottom))

    @property
    def bottomright(self):
        return np.array((self.right, self.bottom))

    def __str__(self):
        text = []
        for attr in ('center', 'size', 'topright', 'bottomleft'):
            text.append(f"{attr}={getattr(self, attr)}")
        return "Rect(" + ', '.join(text) + ')'
