import numpy as np

from objects import Object
from player import Player
from constants import *
from viewport import Viewport


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

        self.player.recheck_for_ground = False
        if self.player.check_for_ground_after is not None:
            if self.player.position[0] >= self.player.check_for_ground_after:
                self.player.on_ground = False
                self.player.recheck_for_ground = True

        small_player_box = self.player.small_bounding_box
        big_player_box = self.player.big_bounding_box

        alignement_tolerance = (-SOLID_ALIGNEMENT_TOLERANCE_ON_GROUND if self.player.recheck_for_ground else -SOLID_ALIGNEMENT_TOLERANCE)

        for obj in self.objects:
            if big_player_box.collide_rect(obj.bounding_box):
                distance_to_top = big_player_box.bottom - obj.bounding_box.top
                if distance_to_top > alignement_tolerance:
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



    def draw(self, viewport: Viewport):
        for obj in self.objects:
            obj.draw(viewport)

        self.player.draw(viewport)

    def stop(self):
        self.stopped = True
