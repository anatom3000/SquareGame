from __future__ import annotations

from functools import cache

import pygame

from rect import Rect


def lerp(a, b, x):
    return (1 - x) * a + x * b


@cache
def scale_texture(source: pygame.Surface, rect_size: (float, float)) -> pygame.Surface:
    return pygame.transform.scale(source, rect_size)


@cache
def rotate_texture(texture, angle, hflip, vflip):
    texture = pygame.transform.flip(texture, hflip, vflip)
    texture = pygame.transform.rotate(texture, -angle)

    return texture


class Viewport:
    def __init__(self, destination: pygame.Surface, zoom: float = 1.0, position: (float, float) = (0.0, 0.0)):
        self.position = position
        self.zoom = zoom

        self.target_position = self.position
        self.target_zoom = self.zoom

        self.destination = destination
        self.resolution = destination.get_size()

        self.position_smoothing_speed = 2.0
        self.zoom_smoothing_speed = 0.5

    def zoom_in(self, delta: float):
        self.target_zoom *= delta
        self.target_position = (
            self.target_position[0] * delta,
            self.target_position[1] * delta,
        )

    def zoom_out(self, delta: float):
        self.target_zoom /= delta
        self.target_position /= delta

    def convert_position(self, position: (float, float)) -> (float, float):
        return (
            + self.zoom * position[0] + self.resolution[0] / 2 - self.position[0],
            - self.zoom * position[1] + self.resolution[1] / 2 - self.position[1],
        )

    def convert_distance(self, distance: float) -> float:
        return distance * self.zoom

    def convert_rect(self, rect: Rect) -> pygame.Rect:
        pg_rect = pygame.Rect((0, 0, 0, 0))
        
        try:
            pg_rect.size = (rect.size[0] * self.zoom, rect.size[1] * self.zoom)
            pg_rect.center = self.convert_position(rect.center)
        except TypeError:
            pass
            
        return pg_rect

    def convert_position_from_screen(self, position: (float, float)):
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
        delta_zoom = lerp(self.zoom, self.target_zoom, dt * self.zoom_smoothing_speed) / self.zoom

        self.position = (
            delta_zoom * lerp(self.position[0], self.target_position[0], dt * self.position_smoothing_speed),
            delta_zoom * lerp(self.position[1], self.target_position[1], dt * self.position_smoothing_speed),
        )

        self.zoom *= delta_zoom

    def blit(self, source: pygame.Surface, rect: Rect):
        rect = self.convert_rect(rect)

        self.destination.blit(scale_texture(source, rect.size), rect)

    def blit_rotated(self, source: pygame.Surface, rect: Rect, angle: float, hflip: bool, vflip: bool):
        old_rect = source.get_rect().copy()
        source = rotate_texture(source, angle, hflip, vflip)
        new_rect = source.get_rect().copy()
        
        rect.size = (
            rect.size[0] * new_rect.w / old_rect.w,
            rect.size[1] * new_rect.h / old_rect.h,
        )

        self.blit(source, rect)

    def draw_rect(self, color: tuple[int, int, int], rect: Rect, width: float | int = 0, widthInPx: bool = False):
        rect = self.convert_rect(rect)

        if width == 0.0:
            width = 0
        elif not widthInPx:
            width = int(self.convert_distance(width))

        pygame.draw.rect(self.destination, color, rect, width)
