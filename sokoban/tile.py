import arcade
from enum import IntEnum, auto


TILE_TEXTURE_SIZE = 64


class TileType(IntEnum):
    EMPTY = auto()
    FLOOR = auto()
    WALL = auto()
    GOAL = auto()
    BOX = auto()


TILE_DEFINITIONS = {
    # Wall
    '#': ('sokoban_tilesheet.png', 7, 8, TILE_TEXTURE_SIZE, TileType.WALL),
    # Floor, floor under box, floor under player
    ' ': ('sokoban_tilesheet.png', 0, 11, TILE_TEXTURE_SIZE, TileType.FLOOR),
    '$': ('sokoban_tilesheet.png', 0, 11, TILE_TEXTURE_SIZE, TileType.FLOOR),
    '@': ('sokoban_tilesheet.png', 0, 11, TILE_TEXTURE_SIZE, TileType.FLOOR),
    # Goal, goal under box, goal under player
    '.': ('sokoban_tilesheet.png', 1, 11, TILE_TEXTURE_SIZE, TileType.GOAL),
    '*': ('sokoban_tilesheet.png', 1, 11, TILE_TEXTURE_SIZE, TileType.FLOOR),
    '+': ('sokoban_tilesheet.png', 1, 11, TILE_TEXTURE_SIZE, TileType.GOAL)
}


class Tile(arcade.Sprite):
    def __init__(self, filename: str, row: int, col: int, tile_size: int):
        super().__init__(filename, scale=1, image_x=col*tile_size, image_y=row*tile_size, image_height=tile_size, image_width=tile_size)

        # reference to box at this location, if any
        self.box_here: Tile = None
