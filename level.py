import numpy as np

from objects import Object
from player import Player
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


def check_collision_solid_top(aabb1: tuple[np.ndarray, np.ndarray], aabb2: tuple[np.ndarray, np.ndarray]):
    # Extract the x and y coordinates of the top-left and bottom-right corners of the two AABBs
    top1 = aabb1[0][1]
    bottom1 = aabb1[1][1]
    top2 = aabb2[0][1]
    bottom2 = aabb2[1][1]

    return bottom1 > top2 and top1 > top2


class Level:
    def __init__(self, objects: list[Object]):
        self.player = Player(position=np.array([0.0, 105]))

        self.objects = objects

        self.input_activated = False
        self.stopped = False

    def tick(self, dt: float):
        if self.stopped:
            return

        self.player.velocity[0] = PLAYER_SPEED

        if not self.player.on_ground:
            self.player.velocity[1] -= PLAYER_GRAVITY * dt

        if self.input_activated:
            self.player.jump()
        if self.player.check_for_ground_after is not None:
            if self.player.position[0] >= self.player.check_for_ground_after:
                self.player.on_ground = False

        small_player_box = self.player.small_bounding_box
        big_player_box = self.player.big_bounding_box

        for obj in self.objects:
            if big_player_box.collide_rect(obj.bounding_box):
                if not self.player.on_ground:
                    distance_to_top = big_player_box.bottom - obj.bounding_box.top
                    if distance_to_top > -SOLID_ALIGNEMENT_TOLERANCE:
                        self.player.align_to_object(obj)
                        self.player.on_ground = True
                        if self.input_activated:
                            self.player.jump()
                        else:
                            self.player.velocity[1] = 0.0

                if small_player_box.collide_rect(obj.bounding_box):
                    self.stop()

        self.player.position += self.player.velocity * dt

        if self.player.position[1] < GROUND_HEIGHT + self.player.big_hitbox[1] / 2:
            self.player.position[1] = GROUND_HEIGHT + self.player.big_hitbox[1] / 2
            self.player.on_ground = True
            self.player.check_for_ground_after = None

    def draw(self, viewport: Viewport):
        for obj in self.objects:
            obj.draw(viewport)

        self.player.draw(viewport)

    def stop(self):
        self.stopped = True
