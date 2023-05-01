import numpy as np

from objects import Player, Object
from constants import *
from viewport import Viewport


def check_collision(aabb1: tuple[np.ndarray, np.ndarray], aabb2: tuple[np.ndarray, np.ndarray]):
    # Extract the x and y coordinates of the top-left and bottom-right corners of the two AABBs
    x1, y1 = aabb1[0]
    x2, y2 = aabb1[1]
    x3, y3 = aabb2[0]
    x4, y4 = aabb2[1]

    if x2 < x3 or x4 < x1:
        return False

    if y2 < y3 or y4 < y1:
        return False

    return True


class Level:
    def __init__(self, objects: list[Object]):
        self.player = Player(position=np.array([0.0, 0.0]))

        self.objects = objects

        self.player_is_holding = False

    def tick(self, dt: float):
        self.player.velocity[0] = PLAYER_SPEED

        self.player.velocity[1] += PLAYER_GRAVITY * dt

        if self.player_is_holding and self.player.on_ground:
            self.player.on_ground = False
            self.player.velocity[1] = -JUMP_VELOCITY

        self.player.position += self.player.velocity * dt

        if self.player.position[1] > 0.0:
            self.player.position[1] = 0.0
            self.player.on_ground = True

        player_box = self.player.solid_bounding_box

        for obj in self.objects:
            if check_collision(player_box, obj.bounding_box):
                print("touched!")

    def draw(self, viewport: Viewport):
        for obj in self.objects:
            obj.draw(viewport)

        self.player.draw(viewport)