from __future__ import annotations

from math import tanh

import numpy as np
import pygame

from rect import Rect


def lerp(a, b, x):
    return (1 - x) * a + x * b


class Viewport:
    def __init__(self, destination: pygame.Surface, zoom: float = 2.0, position: np.ndarray = None):
        self._position = np.array([0.0, 0.0]) if position is None else position
        self._zoom = zoom

        self._target_position = self._position
        self._target_zoom = self._zoom

        self.destination = destination
        self.resolution = np.array(destination.get_size())

        self.position_smoothing_speed = 5.0
        self.zoom_smoothing_speed = 0.5

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: np.ndarray):
        self._target_position = value

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        self._target_zoom = value

    def move(self, delta: np.ndarray):
        self.position += delta

    def zoom_in(self, delta: float):
        self.zoom *= delta
        self.position *= delta

    def zoom_out(self, delta: float):
        self.zoom /= delta
        self.position /= delta

    def convert_position(self, position: np.ndarray) -> np.ndarray:
        return self.zoom * position * (1, -1) + self.resolution / 2 - self.position

    def convert_distance(self, distance: float | np.ndarray) -> float | np.ndarray:
        return distance * self.zoom

    def tick(self, dt: float):
        self._position = lerp(self._position, self._target_position, dt * self.position_smoothing_speed)
        delta_zoom = lerp(self._zoom, self._target_zoom, dt * self.zoom_smoothing_speed) / self._zoom
        self._position *= delta_zoom
        self._zoom *= delta_zoom

    def blit(self, source: pygame.Surface, center: np.ndarray, size: np.ndarray):
        rect = source.get_rect()

        rect.size = self.convert_distance(size)
        rect.center = self.convert_position(center)

        self.destination.blit(source, rect)

    def draw_rect(self, color: tuple[int, int, int], rect: Rect, width: float = 1.0):
        pg_rect = pygame.Rect((0, 0, 0, 0))

        pg_rect.size = self.convert_distance(rect.size)
        pg_rect.center = self.convert_position(rect.center)

        if width == 0.0:
            width = 0
        else:
            width = int(self.convert_distance(width))

        pygame.draw.rect(self.destination, color, pg_rect, width)
