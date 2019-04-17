import arcade
import math
from typing import List, Dict, Tuple
from enum import IntEnum, auto


TILE_TEXTURE_SIZE = 64
TILE_SCALE = 1


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


class SokobanLevel:
    def __init__(self, name: str, width: int, height: int, level_lines: List[str]):
        self.name = name
        self._width: int = width
        self._height: int = height
        self._player_start_position: Tuple[int, int] = (0, 0)
        self._grid: List[Tuple[TileType, Tile]] = [(TileType.EMPTY, None)] * (width * height)
        self._tile_sprites: List[Tile] = []
        self._boxes: List[Tile] = []

        y = 0
        for line in level_lines:
            x = 0
            first_wall = False
            for c in line:
                index = y * self._width + x
                # get rid of preceding empty spaces
                if not first_wall and c == ' ':
                    x += 1
                    continue

                # once we hit a wall, stop ignoring empty spaces
                if c == '#':
                    first_wall = True
                
                if c in TILE_DEFINITIONS:
                    sprite = Tile(*TILE_DEFINITIONS[c][:-1])
                    sprite.center_x = x * TILE_TEXTURE_SIZE
                    sprite.center_y = (self._height - 1 - y) * TILE_TEXTURE_SIZE
                    self._grid[index] = (
                        TILE_DEFINITIONS[c][-1],
                        sprite
                    )

                    # create box
                    if c == '$' or c == '*':                        
                        box_sprite = Tile('sokoban_tilesheet.png', 0, 6, TILE_TEXTURE_SIZE)
                        box_sprite.center_x = x * TILE_TEXTURE_SIZE
                        box_sprite.center_y = (self._height - 1 - y) * TILE_TEXTURE_SIZE
                        self._boxes.append(box_sprite)
                        sprite.box_here = box_sprite

                # player starting position
                if c == '@' or c == '+':
                    self._player_start_position = (x, y)

                x += 1
            y += 1

        # create player and set position
        self.player_sprite: Tile = Tile('sokoban_tilesheet.png', 5, 7, TILE_TEXTURE_SIZE)
        self.player_sprite.center_x = self._player_start_position[0] * TILE_TEXTURE_SIZE
        self.player_sprite.center_y = (self._height - 1 - self._player_start_position[1]) * TILE_TEXTURE_SIZE

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def player_x(self) -> int:
        return self._player_start_position[0]

    @player_x.setter
    def player_x(self, v: int):
        self._player_start_position = (
            v,
            self._player_start_position[1]
        )
        self.player_sprite.center_x = self._player_start_position[0] * TILE_TEXTURE_SIZE

    @property
    def player_y(self) -> int:
        return self._player_start_position[1]

    @player_y.setter
    def player_y(self, v: int):
        self._player_start_position = (
            self._player_start_position[0],
            v
        )
        self.player_sprite.center_y = (self._height - 1 - self._player_start_position[1]) * TILE_TEXTURE_SIZE

    def tile_at(self, x: int, y: int) -> Tuple[TileType, Tile]:
        return self._grid[y * self._width + x]

    def tile_type_at(self, x: int, y: int) -> TileType:
        return self.tile_at(x, y)[0]

    def blocks_push(self, x: int, y: int) -> bool:
        tile_type, tile_sprite = self.tile_at(x, y)
        return tile_type == TileType.WALL or tile_type == TileType.EMPTY or (tile_sprite is not None and tile_sprite.box_here is not None)

    def draw(self):

        # tiles
        for tile_type, tile_sprite in self._grid:
            if tile_type == TileType.EMPTY:
                continue
            if not tile_sprite.box_here:
                tile_sprite.draw()
            else:
                tile_sprite.box_here.draw()

        # draw player
        self.player_sprite.draw()


class SokobanGame(arcade.Window):

    def __init__(self):
        # set up the window with size and title
        super().__init__(800, 600, 'Sokoban')

        # set the background color
        arcade.set_background_color(arcade.color.BLACK)

        self.levels = []
        self._load_level_file('levels.txt')

        self.active_level = None
        self.active_level_index = 0
        self.play_level(0)

        self.last_frame = 1

    def _parse_level(self, level_lines: List[str]) -> dict:
        width = max([len(line) for line in level_lines])
        height = len(level_lines) - 1
        level_name = ''
        lines = []
        for line in level_lines:            
            if line.startswith(';'):
                level_name = line[1:]
            else:                
                lines.append(line)    

        return {
            'name': level_name,
            'width': width,
            'height': height,
            'lines': lines
        }

    def _load_level_file(self, file_path: str):
        self.levels = []
        with open(file_path, 'r') as levels_file:
            all_lines = levels_file.read().split('\n')
            level_breaks = []
            for index, line in enumerate(all_lines):                
                if len(line.strip()) == 0:
                    level_breaks.append(index)
            start = 0
            for index in level_breaks:
                self.levels.append(self._parse_level(all_lines[start:index]))
                start = index

    def play_level(self, level_index: int):
        level = self.levels[level_index]
        self.active_level_index = level_index
        self.active_level = SokobanLevel(level['name'], level['width'], level['height'], level['lines'])

    def on_draw(self):
        """ Handle drawing here. """
        arcade.start_render()

        width, height = self.get_size()

        # zoom out and center
        scaled_width = int(width * 2)
        scaled_height = int(height * 2)

        center_x = int(self.active_level.width * TILE_TEXTURE_SIZE / 2)
        center_y = int(self.active_level.height * TILE_TEXTURE_SIZE / 2)

        arcade.set_viewport(
            -center_x,
            -center_x + scaled_width,
            -center_y,
            -center_y + scaled_height
        )

        self.active_level.draw()

        # reset viewport
        arcade.set_viewport(0, width, 0, height)
        # draw framerate in bottom-left corner
        arcade.draw_text(f'FPS: {round(1.0 / self.last_frame, 1)}', 5, 5, arcade.color.RED, 12)

    def on_update(self, delta):
        self.last_frame = delta
        screen_width, screen_height = self.get_size()

    def _move_player(self, delta_x: int, delta_y: int):
        new_x = self.active_level.player_x + delta_x
        new_y = self.active_level.player_y + delta_y

        tile_type, tile_sprite = self.active_level.tile_at(new_x, new_y)
        if tile_type != TileType.WALL and tile_type != TileType.EMPTY:
            # is there a box, and can we push it?
            if not tile_sprite.box_here:
                self.active_level.player_x = new_x
                self.active_level.player_y = new_y
            else:
                # get next space in same direction
                push_x = new_x + delta_x
                push_y = new_y + delta_y                
                if not self.active_level.blocks_push(push_x, push_y):
                    # move block and player
                    box = tile_sprite.box_here
                    tile_sprite.box_here = None
                    new_tile = self.active_level.tile_at(push_x, push_y)[1]
                    new_tile.box_here = box
                    box.center_x = new_tile.center_x
                    box.center_y = new_tile.center_y
                    self.active_level.player_x = new_x
                    self.active_level.player_y = new_y

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # kill the game
            arcade.close_window()
        elif key == arcade.key.F2:
            # restart current level
            self.play_level(self.active_level_index)

        if key == arcade.key.LEFT:
            self._move_player(-1, 0)
        elif key == arcade.key.RIGHT:
            self._move_player(1, 0)
        elif key == arcade.key.UP:
            self._move_player(0, -1)
        elif key == arcade.key.DOWN:
            self._move_player(0, 1)


if __name__ == '__main__':

    game = SokobanGame()
    arcade.run()
