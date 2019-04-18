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
        self.finished_level = False
        self.play_level(0)

        self.last_frame = 1
        self.show_fps = False

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
        self.finished_level = False
        self.active_level_index = level_index
        self.active_level = SokobanLevel(level['name'], level['width'], level['height'], level['lines'])

    def on_draw(self):
        """ Handle drawing here. """
        arcade.start_render()

        width, height = self.get_size()

        # zoom out to fit entire level on screen
        scale = self.active_level.screen_scale(width, height)
        scaled_width = int(width * scale)
        scaled_height = int(height * scale)        

        # offset center to be over the middle of the level
        center_x = self.active_level.center_x - TILE_TEXTURE_SIZE * 0.5
        center_y = self.active_level.center_y - TILE_TEXTURE_SIZE        

        arcade.set_viewport(
            center_x - scaled_width / 2,
            center_x + scaled_width / 2,
            center_y - scaled_height / 2,
            center_y + scaled_height / 2
        )

        self.active_level.draw()

        # reset viewport
        arcade.set_viewport(0, width, 0, height)

        # if level is won, show message
        if self.finished_level:
            arcade.draw_text('COMPLETE!', width / 2, height / 2, arcade.color.YELLOW, 64, anchor_x='center')

        # draw framerate in bottom-left corner
        if self.show_fps:
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
        elif key == arcade.key.F1:
            # toggle FPS meter
            self.show_fps = not self.show_fps

        elif self.active_level and not self.finished_level:
            # handle movement and check for win
            if key == arcade.key.LEFT:
                self.active_level.move_player(-1, 0)
                self.finished_level = self.active_level.check_win()
            elif key == arcade.key.RIGHT:
                self.active_level.move_player(1, 0)
                self.finished_level = self.active_level.check_win()
            elif key == arcade.key.UP:
                self.active_level.move_player(0, -1)
                self.finished_level = self.active_level.check_win()
            elif key == arcade.key.DOWN:
                self.active_level.move_player(0, 1)
                self.finished_level = self.active_level.check_win()

        elif self.active_level and self.finished_level and key == arcade.key.SPACE:
            # advance to next level
            next_level_index = self.active_level_index + 1
            if next_level_index >= len(self.levels):
                next_level_index = 0
            self.play_level(next_level_index)



if __name__ == '__main__':

    game = SokobanGame()
    arcade.run()
