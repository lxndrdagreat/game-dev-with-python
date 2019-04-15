from enum import Enum
import math
from typing import Tuple
import arcade


class ThemeColors(Enum):
    FOREGROUND = (arcade.color.AFRICAN_VIOLET, )
    BACKGROUND = (arcade.color.AERO_BLUE, )

    def __init__(self, color):
        self.color = color


def rotate_point(x: int, y: int, ox: int, oy: int, angle_degrees: float) -> Tuple[int, int]:
    angle_rads = round(math.radians(angle_degrees), 2)
    s = math.sin(angle_rads)
    c = math.cos(angle_rads)

    x -= ox
    y -= oy
    newx = round(x * c - y * s, 2) + ox
    newy = round(x * s + y * c, 2) + oy

    return (newx, newy, )


def point_in_polygon(point_x: int, point_y: int, polygon: list) -> bool:
    n = len(polygon)
    inside = False

    x1, y1 = polygon[0]
    for i in range(n + 1):
        x2, y2 = polygon[i % n]
        if point_y > min(y1, y2):
            if point_y <= max(y1, y2):
                if point_x <= max(x1, x2):
                    if y1 != y2:
                        x_intersect = (point_y - y1) * (x2 - x1) / (y2 - y1) + x1
                        if x1 == x2 or point_x <= x_intersect:
                            inside = not inside
        x1, y1 = x2, y2

    return inside
