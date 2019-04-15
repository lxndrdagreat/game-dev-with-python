import arcade
from utils import ThemeColors
from typing import Tuple
import math


class Bullet:
    def __init__(self, position: Tuple[int, int], angle: float):
        self.x = position[0]
        self.y = position[1]
        self.angle_radians = round(math.radians(angle), 2)        
        self.alive = True

        # maximum lifespan of the bullet in seconds
        self.lifetime = 2.0

        # movement speed in pixels per second
        self.speed = 400

        # direction vector
        self.velocity_x = self.speed * math.cos(self.angle_radians)
        self.velocity_y = self.speed * math.sin(self.angle_radians)

    def update(self, delta_time: float):
        self.lifetime -= delta_time
        if self.lifetime <= 0:
            self.alive = False
            return

        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        # TODO: wrap the bullets when they exit the screen space

    def draw(self):
        arcade.draw_point(self.x, self.y, ThemeColors.FOREGROUND.color, 5)
