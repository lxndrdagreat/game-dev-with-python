import arcade
import math
from typing import List, Tuple
import random
from enum import Enum, IntFlag
import random
import datetime
import os


class BoardSize(Enum):
    BEGINNER = (9, 9, 10)
    INTERMEDIATE = (16, 16, 40)
    ADVANCED = (24, 24, 99)

    def __init__(self, width: int, height: int, mine_count: int):
        self.width = width
        self.height = height
        self.mine_count = mine_count
    
    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height


class CellState(IntFlag):
    EMPTY = 1
    IS_MINE = 2
    NEIGHBOR_NORTH = 4
    NEIGHBOR_SOUTH = 8
    NEIGHBOR_EAST = 16
    NEIGHBOR_WEST = 32
    NEIGHBOR_NORTH_EAST = 64
    NEIGHBOR_SOUTH_EAST = 128
    NEIGHBOR_NORTH_WEST = 256
    NEIGHBOR_SOUTH_WEST = 512
    DISCOVERED = 1024
    MARKED = 2048

NEIGHBOR_FLAGS = (
    CellState.NEIGHBOR_NORTH,
    CellState.NEIGHBOR_SOUTH,
    CellState.NEIGHBOR_EAST,
    CellState.NEIGHBOR_WEST,
    CellState.NEIGHBOR_NORTH_EAST,
    CellState.NEIGHBOR_NORTH_WEST,
    CellState.NEIGHBOR_SOUTH_EAST,
    CellState.NEIGHBOR_SOUTH_WEST
)

class MinesweeperGame(arcade.Window):

    def __init__(self):
        # set up the window with size and title
        super().__init__(500, 600, 'Minesweeper')

        self.resource_path = os.path.dirname(os.path.abspath(__file__))

        # load and set the icon
        # using underlying Pyglet functionality
        # https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/windowing.html
        icon = arcade.pyglet.image.load(os.path.join(self.resource_path, 'icon64.png'))
        self.set_icon(icon)

        # set the background color
        arcade.set_background_color(arcade.color.BLACK)        

        # difficulty is determined by the size of the board
        self.difficulty: BoardSize = BoardSize.BEGINNER

        # single-dimension list that will represent our board state
        self.board: List[CellState] = []

        # used to determine framerate
        self.last_frame = 1
        self.board_sprites: List[arcade.Sprite] = []      

        self.start_time = 0
        self.is_game_over = False
        self.new_game(BoardSize.BEGINNER)

    def new_game(self, difficulty: BoardSize):
        """ Starts a new game with the provided difficulty """
        self.difficulty = difficulty
        self.start_time = 0
        self.is_game_over = False
        board_width, board_height = difficulty.size
        
        # create grid of empty cells
        self.board = [CellState.EMPTY] * (board_width * board_height)
        
        # randomly put mines in empty cells
        for i in range(0, difficulty.mine_count):
            index = random.randint(0, len(self.board) - 1)
            while CellState.IS_MINE in self.board[index]:
                index = random.randint(0, len(self.board) - 1)
            
            self.board[index] = CellState.IS_MINE

        start_x = 0
        start_y = 500
        cell_size = math.floor(500 / self.difficulty.width)
        cell_buffer = (500 - cell_size * self.difficulty.width) / 2
        sprite_scale = cell_size / 64  # size of the button image
        self.board_sprites = [None] * len(self.board)
        for y in range(0, board_height):
            for x in range(0, board_width):
                index = y * board_width + x
                cell = self.board[index]
                # neighbors with mines
                
                # north
                if y > 0 and CellState.IS_MINE in self.cell_by_coord(x, y - 1):
                    cell = cell | CellState.NEIGHBOR_NORTH
                # north-east
                if y > 0 and x < board_width - 1 and CellState.IS_MINE in self.cell_by_coord(x + 1, y - 1):
                    cell = cell | CellState.NEIGHBOR_NORTH_EAST
                # east
                if x < board_width - 1 and CellState.IS_MINE in self.cell_by_coord(x + 1, y):
                    cell = cell | CellState.NEIGHBOR_EAST
                # south-east
                if x < board_width - 1 and y < board_height - 1 and CellState.IS_MINE in self.cell_by_coord(x + 1, y + 1):
                    cell = cell | CellState.NEIGHBOR_SOUTH_EAST
                # south
                if y < board_height - 1 and CellState.IS_MINE in self.cell_by_coord(x, y + 1):
                    cell = cell | CellState.NEIGHBOR_SOUTH
                # south-west
                if x > 0 and y < board_height - 1 and CellState.IS_MINE in self.cell_by_coord(x - 1, y + 1):
                    cell = cell | CellState.NEIGHBOR_SOUTH_WEST
                # west
                if x > 0 and CellState.IS_MINE in self.cell_by_coord(x - 1, y):
                    cell = cell | CellState.NEIGHBOR_WEST
                # north-west
                if x > 0 and y > 0 and CellState.IS_MINE in self.cell_by_coord(x - 1, y - 1):
                    cell = cell | CellState.NEIGHBOR_NORTH_WEST

                self.board[index] = cell

                # sprite
                button = arcade.Sprite(os.path.join(self.resource_path, 'button.png'))
                button.scale = sprite_scale
                button.center_x = start_x + cell_buffer + (cell_size * x + cell_size / 2)
                button.center_y = start_y - cell_buffer - (cell_size * y + cell_size / 2)
                self.board_sprites[index] = button

    def cell_by_coord(self, x, y) -> CellState:
        return self.board[y * self.difficulty.width + x]

    def sum_neighbor_flags(self, x: int, y: int) -> int:
        index = y * self.difficulty.width + x
        cell = self.board[index]
        return self.cell_neighbor_count(cell)

    def cell_neighbor_count(self, cell: CellState) -> int:
        return len([flag for flag in NEIGHBOR_FLAGS if flag in cell])

    def on_draw(self):
        """ Handle drawing here. """
        arcade.start_render()

        # top display area
        arcade.draw_rectangle_filled(250, 550, 500, 100, arcade.color.BLACK_OLIVE)
        # draw time
        draw_time = str(datetime.timedelta(seconds=math.floor(self.start_time)))
        arcade.draw_text(draw_time, 25, 550, arcade.color.YELLOW if not self.is_game_over else arcade.color.RED, 16)

        # grid
        start_x = 0
        start_y = 500
        cell_size = math.floor(500 / self.difficulty.width)
        cell_buffer = (500 - cell_size * self.difficulty.width) / 2

        for index, cell in enumerate(self.board):        
            sprite = self.board_sprites[index]
            sprite.draw()
            
            if CellState.DISCOVERED in cell:
                if CellState.IS_MINE not in cell:
                    neighbor_count = self.cell_neighbor_count(cell)
                    if neighbor_count > 0:
                        arcade.draw_text(str(neighbor_count), sprite.center_x, sprite.center_y, arcade.color.BLACK, 16)

        # draw framerate in bottom-left corner
        # arcade.draw_text(f'FPS: {round(1.0 / self.last_frame, 1)}', 5, 5, arcade.color.YELLOW, 12)

    def on_update(self, delta):
        self.last_frame = delta
        if not self.is_game_over:
            self.start_time += delta

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # kill the game
            arcade.close_window()
        elif key == arcade.key.F2:
            # start a new game with same difficulty
            self.new_game(self.difficulty)

    def flood_empty_cells(self, start_x, start_y):
        """ Recursive flood-fill to mark empty cells (with no neighbors) as discovered """
        cell = self.cell_by_coord(start_x, start_y)
        if CellState.EMPTY not in cell or CellState.DISCOVERED in cell or self.cell_neighbor_count(cell) > 0:
            return
        # mark the cell as discovered
        cell = cell | CellState.DISCOVERED
        self.board[start_y * self.difficulty.width + start_x] = cell
        old_sprite = self.board_sprites[start_y * self.difficulty.width + start_x]                    
        sprite = arcade.Sprite(os.path.join(self.resource_path, 'button_pressed.png'))
        sprite.scale = old_sprite.scale
        sprite.center_x = old_sprite.center_x
        sprite.center_y = old_sprite.center_y
        self.board_sprites[start_y * self.difficulty.width + start_x] = sprite           

        # flood to neighbors
        deltas = (-1, 0, 1)
        for y_delta in deltas:
            y = y_delta + start_y
            if y < 0 or y >= self.difficulty.height:
                continue
            for x_delta in deltas:
                x = x_delta + start_x
                if x < 0 or x >= self.difficulty.width:
                    continue
                self.flood_empty_cells(x, y)

    def activate_cell(self, x, y):
        if x < 0 or x >= self.difficulty.width or y < 0 or y >= self.difficulty.height:                
            raise Exception(f'Position {x}, {y} is outside the board.')
        index = y * self.difficulty.width + x
        cell = self.board[index]
        # can't click on an already-discovered cell, or if the cell is currently marked.
        if CellState.DISCOVERED not in cell and CellState.MARKED not in cell:
            if CellState.EMPTY in cell and self.cell_neighbor_count(cell) == 0:
                self.flood_empty_cells(x, y)
            cell = cell | CellState.DISCOVERED
            self.board[index] = cell
            old_sprite = self.board_sprites[index]            
            sprite: arcade.Sprite
            if CellState.IS_MINE in cell:            
                self.is_game_over = True
                sprite = arcade.Sprite(os.path.join(self.resource_path, 'mine-explosion.png'))
            else:
                sprite = arcade.Sprite(os.path.join(self.resource_path, 'button_pressed.png'))
            sprite.scale = old_sprite.scale
            sprite.center_x = old_sprite.center_x
            sprite.center_y = old_sprite.center_y
            self.board_sprites[index] = sprite            

    def mark_cell(self, x, y):
        if x < 0 or x >= self.difficulty.width or y < 0 or y >= self.difficulty.height:                
            raise Exception(f'Position {x}, {y} is outside the board.')
        index = y * self.difficulty.width + x
        cell = self.board[index]
        if CellState.DISCOVERED not in cell:
            old_sprite = self.board_sprites[index]
            sprite: arcade.Sprite
            if CellState.MARKED in cell:
                # unmark
                cell = cell ^ CellState.MARKED
                sprite = arcade.Sprite(os.path.join(self.resource_path, 'button.png'))
            else:
                # mark
                cell = cell | CellState.MARKED
                sprite = arcade.Sprite(os.path.join(self.resource_path, 'button_marked.png'))
            self.board[index] = cell
            sprite.scale = old_sprite.scale
            sprite.center_x = old_sprite.center_x
            sprite.center_y = old_sprite.center_y
            self.board_sprites[index] = sprite

    def mouse_position_to_grid_position(self, mouse_x, mouse_y) -> Tuple[int, int]:
        cell_size = math.floor(500 / self.difficulty.width)            
        cell_buffer = (500 - cell_size * self.difficulty.width) / 2
        x = mouse_x - cell_buffer
        y = mouse_y - cell_buffer
        if x < 0 or x > 500 - cell_buffer * 2 or y < 0 or y > 500 - cell_buffer * 2:
            # make sure click was inside grid area
            return -1, -1
        grid_x = math.floor(x / cell_size)
        grid_y = self.difficulty.height - 1 - math.floor(y / cell_size)
        return grid_x, grid_y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_game_over:
            return
        if button == arcade.MOUSE_BUTTON_LEFT:            
            # select cell
            grid_x, grid_y = self.mouse_position_to_grid_position(x, y)
            if grid_x < 0 or grid_x >= self.difficulty.width or grid_y < 0 or grid_y >= self.difficulty.height:                
                return
            self.activate_cell(grid_x, grid_y)
        
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # mark/unmark cell
            grid_x, grid_y = self.mouse_position_to_grid_position(x, y)
            if grid_x < 0 or grid_x >= self.difficulty.width or grid_y < 0 or grid_y >= self.difficulty.height:                
                return
            self.mark_cell(grid_x, grid_y)


if __name__ == '__main__':
    game = MinesweeperGame()
    arcade.run()
