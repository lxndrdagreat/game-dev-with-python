import arcade
import math
from typing import List


class SokobanGame(arcade.Window):

    def __init__(self):
        # set up the window with size and title
        super().__init__(800, 600, 'Sokoban')

        # set the background color
        arcade.set_background_color(arcade.color.BLACK)
        
        self.levels = []
        self._load_level_file('levels.txt')

        self.last_frame = 1

    def _parse_level(self, level_lines: List[str]):
        print()
        width = 0
        height = 0
        level_name = ''
        for line in level_lines:
            if line.startswith(';'):
                level_name = line[1:]
            else:
                height += 1
                width = max(width, len(line))
                print(line)


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
                print(start, index)
                self._parse_level(all_lines[start:index])
                start = index


    def on_draw(self):
        """ Handle drawing here. """
        arcade.start_render()

        # draw framerate in bottom-left corner
        arcade.draw_text(f'FPS: {round(1.0 / self.last_frame, 1)}', 5, 5, arcade.color.BLACK, 12)

    def on_update(self, delta):
        self.last_frame = delta
        screen_width, screen_height = self.get_size()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # kill the game
            arcade.close_window()


if __name__ == '__main__':

    game = SokobanGame()
    arcade.run()
