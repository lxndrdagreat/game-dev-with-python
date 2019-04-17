import arcade
from typing import List, Dict, Tuple
from enum import IntEnum, auto
from level import SokobanLevel
from tile import TILE_TEXTURE_SIZE


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
        # used to determine FPS
        self.last_frame = delta

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # kill the game
            arcade.close_window()
        elif key == arcade.key.F2:
            # restart current level
            self.play_level(self.active_level_index)

        if self.active_level:
            if key == arcade.key.LEFT:
                self.active_level.move_player(-1, 0)
            elif key == arcade.key.RIGHT:
                self.active_level.move_player(1, 0)
            elif key == arcade.key.UP:
                self.active_level.move_player(0, -1)
            elif key == arcade.key.DOWN:
                self.active_level.move_player(0, 1)


if __name__ == '__main__':

    game = SokobanGame()
    arcade.run()
