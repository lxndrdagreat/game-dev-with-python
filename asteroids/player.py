import math
import arcade
from utils import rotate_point, ThemeColors


class PlayerShip:
    def __init__(self, x: int, y: int):

        self.alive = True

        # x and y will be the center of our triangle
        self.x = x
        self.y = y

        # player's current rotation, in degrees
        # start with the player pointing "up"
        self.rotation = 90

        # how many degrees should the ship rotate per second
        self.rotation_speed = 180

        # acceleration
        self.thrust = 200
        self.acceleration_x = 0
        self.acceleration_y = 0

        # velocity is used to actually update ship position
        self.velocity_x = 0
        self.velocity_y = 0

        # how large to make the player
        self.scale = 10

        # how fast can the player fire bullets, represented as a cooldown
        self.fire_rate = 0.5
        self.cooldown = 0

    def add_rotation(self, sign, delta_time):
        # sign should be 1 or -1
        self.rotation += sign * self.rotation_speed * delta_time

    def add_acceleration(self):
        rotation_rads = round(math.radians(self.rotation), 2)
        self.acceleration_x += self.thrust * math.cos(rotation_rads)
        self.acceleration_y += self.thrust * math.sin(rotation_rads)

    def apply_velocity(self, delta_time):
        # TODO: it would probably be smart to implement a max speed
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        self.velocity_x += self.acceleration_x * delta_time
        self.velocity_y += self.acceleration_y * delta_time
        self.acceleration_x = 0
        self.acceleration_y = 0

    def rotated_points(self) -> tuple:
        # define the points of the ship's triangle and rotate them by the player's rotation    
        point_nose = rotate_point(self.x + self.scale, self.y, self.x, self.y, self.rotation)
        point_right_fin = rotate_point(self.x - self.scale, self.y - (self.scale * 0.8), self.x, self.y, self.rotation)
        point_left_fin = rotate_point(self.x - self.scale, self.y + (self.scale * 0.8), self.x, self.y, self.rotation)

        return point_nose, point_right_fin, point_left_fin

    def draw(self):

        # define the points of the ship's triangle and rotate them by the player's rotation    
        point_nose, point_right_fin, point_left_fin = self.rotated_points()

        # draw a filled triangle based on the three points from above
        arcade.draw_triangle_filled(
            point_nose[0], point_nose[1],
            point_right_fin[0], point_right_fin[1],
            point_left_fin[0], point_left_fin[1],
            ThemeColors.FOREGROUND.color
        )

    def update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time

    def fire(self) -> bool:
        if self.cooldown > 0:
            return False

        self.cooldown = self.fire_rate
        return True
