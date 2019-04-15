import arcade
from enum import IntEnum
from utils import ThemeColors, rotate_point, point_in_polygon
import random
import math


class AsteroidSize(IntEnum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class Asteroid:
    def __init__(self, x: int, y: int, size: AsteroidSize = AsteroidSize.LARGE):
        self.x = x
        self.y = y

        self.alive = True
        
        # add some random rotation
        self.rotation = random.randint(0, 360)

        # is this a large, medium or small asteroid?
        self.size = size
        self.scale = (20, 30, 40)[self.size.value]

        # speed will be based on size
        self.speed = (200, 150, 70)[self.size.value]
        rads = round(math.radians(self.rotation), 2)
        self.velocity_x = math.cos(rads) * self.speed
        self.velocity_y = math.sin(rads) * self.speed

    def _rotated_points(self) -> list:
        point_list = [
            [self.x - (self.scale / 2), self.y + self.scale],
            [self.x + (self.scale / 2), self.y + self.scale],
            [self.x + self.scale, self.y],
            [self.x + (self.scale / 2), self.y - (self.scale / 2)],
            [self.x + (self.scale / 2), self.y - self.scale],
            [self.x, self.y - self.scale],
            [self.x - (self.scale / 2), self.y - (self.scale / 2)],
            [self.x - self.scale, self.y - (self.scale / 4)],
            [self.x - self.scale, self.y]
        ]

        # rotate the points
        for i in range(0, len(point_list)):
            point = point_list[i]
            point_list[i] = rotate_point(point[0], point[1], self.x, self.y, self.rotation)

        return point_list

    def update(self, delta_time: float, screen_width: int, screen_height: int):
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

        # wrap around screen
        if self.x < -self.scale:
            self.x = screen_width + self.scale / 2
        elif self.x > screen_width + self.scale / 2:
            self.x = -self.scale
        if self.y < -self.scale:
            self.y = screen_height + self.scale / 2
        elif self.y > screen_height + self.scale / 2:
            self.y = -self.scale
        
    def collides_with_point(self, x: int, y: int) -> bool:
        points = self._rotated_points()
        return point_in_polygon(x, y, points)

    def draw(self):
        point_list = self._rotated_points()
        arcade.draw_polygon_filled(point_list, ThemeColors.FOREGROUND.color)
