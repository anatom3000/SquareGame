from __future__ import annotations

from functools import cache
from math import tanh

import numpy as np
import pygame

from rect import Rect


def lerp(a, b, x):
    return (1 - x) * a + x * b

@cache
def scale_texture(source: pygame.Surface, rect_size: np.ndarray) -> pygame.Surface:
    return pygame.transform.scale(source, rect_size)

class Viewport:
    def __init__(self, destination: pygame.Surface, zoom: float = 1.0, position: np.ndarray = None):
        self.position = np.array([0.0, 0.0]) if position is None else position
        self.zoom = zoom

        self.target_position = np.copy(self.position)
        self.target_zoom = self.zoom

        self.destination = destination
        self.resolution = np.array(destination.get_size())

        self.position_smoothing_speed = 1.0
        self.zoom_smoothing_speed = 0.5

    def zoom_in(self, delta: float):
        self.target_zoom *= delta
        self.target_position *= delta

    def zoom_out(self, delta: float):
        self.target_zoom /= delta
        self.target_position /= delta

    def convert_position(self, position: np.ndarray) -> np.ndarray:
        return self.zoom * position * (1, -1) + self.resolution / 2 - self.position

    def convert_distance(self, distance: float | np.ndarray) -> float | np.ndarray:
        return distance * self.zoom

    def convert_rect(self, rect: Rect) -> pygame.Rect:
        pg_rect = pygame.Rect((0, 0, 0, 0))

        pg_rect.size = self.convert_distance(rect.size)
        pg_rect.center = self.convert_position(rect.center)

        return pg_rect

    def convert_position_from_screen(self, position: np.array):
        return ((position + self.position - self.resolution / 2) / self.zoom) * (1, -1)

    @property
    def top(self):
        return (0.5 * self.resolution[1] - self.position[1]) / self.zoom

    @property
    def bottom(self):
        return -(0.5 * self.resolution[1] + self.position[1]) / self.zoom

    @property
    def left(self):
        return (self.position[0] - 0.5 * self.resolution[0]) / self.zoom

    @property
    def right(self):
        return (0.5 * self.resolution[0] + self.position[0]) / self.zoom

    @property
    def target_top(self):
        return (0.5 * self.resolution[1] - self.target_position[1]) / self.target_zoom

    @property
    def target_bottom(self):
        return -(0.5 * self.resolution[1] + self.target_position[1]) / self.target_zoom

    @property
    def target_left(self):
        return (self.target_position[0] - 0.5 * self.resolution[0]) / self.target_zoom

    @property
    def target_right(self):
        return (0.5 * self.resolution[0] + self.target_position[0]) / self.target_zoom

    def tick(self, dt: float):
        self.position = lerp(self.position, self.target_position, dt * self.position_smoothing_speed)

        delta_zoom = lerp(self.zoom, self.target_zoom, dt * self.zoom_smoothing_speed) / self.zoom
        self.position *= delta_zoom
        self.zoom *= delta_zoom

    def blit(self, source: pygame.Surface, rect: Rect):
        rect = self.convert_rect(rect)

        self.destination.blit(scale_texture(source, rect.size), rect)

    def draw_rect(self, color: tuple[int, int, int], rect: Rect, width: float = 0.0):
        rect = self.convert_rect(rect)

        if width == 0.0:
            width = 0
        else:
            width = int(self.convert_distance(width))

        pygame.draw.rect(self.destination, color, rect, width)
