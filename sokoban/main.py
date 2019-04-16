import arcade
import math
from typing import List, Dict
from enum import IntEnum, auto


TILE_TEXTURE_SIZE = 64
TILE_SCALE = 1

class TileType(IntEnum):
    FLOOR = auto()
    WALL = auto()
    GOAL = auto()
    BOX = auto()


TILE_DEFINITIONS = {
    '#': ('sokoban_tilesheet.png', 7, 8, TILE_TEXTURE_SIZE, TileType.WALL),
    ' ': ('sokoban_tilesheet.png', 0, 11, TILE_TEXTURE_SIZE, TileType.FLOOR),
    '$': ('sokoban_tilesheet.png', 0, 11, TILE_TEXTURE_SIZE, TileType.FLOOR),
    '@': ('sokoban_tilesheet.png', 0, 11, TILE_TEXTURE_SIZE, TileType.FLOOR),
    '.': ('sokoban_tilesheet.png', 1, 11, TILE_TEXTURE_SIZE, TileType.GOAL),
    '*': ('sokoban_tilesheet.png', 1, 11, TILE_TEXTURE_SIZE, TileType.GOAL),
    '+': ('sokoban_tilesheet.png', 1, 11, TILE_TEXTURE_SIZE, TileType.GOAL)
}


class Tile(arcade.Sprite):
    def __init__(self, filename: str, row: int, col: int, tile_size: int, tile_type: TileType):
        super().__init__(filename, scale=1, image_x=col*tile_size, image_y=row*tile_size, image_height=tile_size, image_width=tile_size)
        self.tile_type = tile_type


class SokobanGame(arcade.Window):

    def __init__(self):
        # set up the window with size and title
        super().__init__(800, 600, 'Sokoban')

        # set the background color
        arcade.set_background_color(arcade.color.BLACK)
        
        self.player = Tile('sokoban_tilesheet.png', 5, 7, TILE_TEXTURE_SIZE, TileType.BOX)

        self.levels = []
        self._load_level_file('levels.txt')

        self.level_tiles: List[Tile] = []
        self.level_boxes: List[Tile] = []
        self.active_level = None
        self.play_level(0)

        self.last_frame = 1
        # self.test_tile: Tile = Tile('sokoban_tilesheet.png', 1, 2, TILE_TEXTURE_SIZE)
        # self.test_tile.center_x = 400
        # self.test_tile.center_y = 300

    def _parse_level(self, level_lines: List[str]) -> dict:
        width = max([len(line) for line in level_lines])
        height = len(level_lines) - 1
        level_name = ''
        tiles = []
        boxes = []
        player_x = 0
        player_y = 0
        y = 0
        for line in level_lines:            
            if line.startswith(';'):
                level_name = line[1:]
            else:                
                x = 0
                for block in line:
                    # handle tiles
                    if block in TILE_DEFINITIONS:
                        tiles.append((
                            block,
                            x,
                            y
                        ))

                        if block == '$' or block == '*':
                            boxes.append((x, y))
                        elif block == '@' or block == '+':
                            player_x = x
                            player_y = y

                    x += 1

                y += 1                

        return {
            'name': level_name,
            'width': width,
            'height': height,
            'tiles': tiles,
            'player': (player_x, player_y),
            'boxes': boxes
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
        self.active_level = level
        self.level_tiles = []
        self.level_boxes = []
        height = level['height']
        width = level['width']

        for tile_data in level['tiles']:
            key, x, y = tile_data
            sprite = Tile(*TILE_DEFINITIONS[key])
            sprite.scale = TILE_SCALE
            sprite.center_x = x * TILE_TEXTURE_SIZE * TILE_SCALE
            sprite.center_y = (height - 1 - y) * TILE_TEXTURE_SIZE
            self.level_tiles.append(sprite)

        for box_data in level['boxes']:
            x, y = box_data
            sprite = Tile('sokoban_tilesheet.png', 0, 6, TILE_TEXTURE_SIZE, TileType.BOX)
            sprite.center_x = x * TILE_TEXTURE_SIZE
            sprite.center_y = (height - 1 - y) * TILE_TEXTURE_SIZE
            self.level_boxes.append(sprite)

        player_x, player_y = level['player']
        self.player.center_x = player_x * TILE_TEXTURE_SIZE
        self.player.center_y = (height - 1 - player_y) * TILE_TEXTURE_SIZE

    def on_draw(self):
        """ Handle drawing here. """
        arcade.start_render()

        width, height = self.get_size()

        # zoom out and center
        scaled_width = int(width * 2)
        scaled_height = int(height * 2)

        center_x = int(self.active_level['width'] * TILE_TEXTURE_SIZE / 2)
        center_y = int(self.active_level['height'] * TILE_TEXTURE_SIZE / 2)

        arcade.set_viewport(
            -center_x,
            -center_x + scaled_width,
            -center_y,
            -center_y + scaled_height
        )

        for sprite in self.level_tiles:
            sprite.draw()
        
        for box in self.level_boxes:
            box.draw()

        self.player.draw()

        # reset viewport
        arcade.set_viewport(0, width, 0, height)
        # draw framerate in bottom-left corner
        arcade.draw_text(f'FPS: {round(1.0 / self.last_frame, 1)}', 5, 5, arcade.color.RED, 12)

    def on_update(self, delta):
        self.last_frame = delta
        screen_width, screen_height = self.get_size()

    def _move_player(self, delta_x: int, delta_y: int):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # kill the game
            arcade.close_window()

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
