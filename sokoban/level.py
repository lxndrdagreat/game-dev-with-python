import arcade
from tile import TILE_DEFINITIONS, TILE_TEXTURE_SIZE, Tile, TileType
from typing import List, Tuple


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
                        box_sprite.center_x = sprite.center_x
                        box_sprite.center_y = sprite.center_y
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

    def screen_scale(self, screen_width: int, screen_height: int) -> float:
        """ Returns the amount of scale needed to fit the entire level on the screen. """
        w = self.width * TILE_TEXTURE_SIZE
        h = self.height * TILE_TEXTURE_SIZE

        w_scale = 1.0 if w < screen_width else round(w / screen_width, 2)
        h_scale = 1.0 if h < screen_height else round(h / screen_height, 2)

        return max(w_scale, h_scale)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def center_x(self) -> int:
        """ Returns the horizontal center of the level in pixels """
        return int(float(self._width) * float(TILE_TEXTURE_SIZE) / 2.0)

    @property
    def center_y(self) -> int:
        """ Returns the vertical center of the level in pixels """
        return int(float(self._height) * float(TILE_TEXTURE_SIZE) / 2.0)

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

    def move_player(self, delta_x: int, delta_y: int):
        new_x = self.player_x + delta_x
        new_y = self.player_y + delta_y

        tile_type, tile_sprite = self.tile_at(new_x, new_y)
        if tile_type != TileType.WALL and tile_type != TileType.EMPTY:
            # is there a box, and can we push it?
            if not tile_sprite.box_here:
                self.player_x = new_x
                self.player_y = new_y
            else:
                # get next space in same direction
                push_x = new_x + delta_x
                push_y = new_y + delta_y                
                if not self.blocks_push(push_x, push_y):
                    # move block and player
                    box = tile_sprite.box_here
                    tile_sprite.box_here = None
                    new_tile = self.tile_at(push_x, push_y)[1]
                    new_tile.box_here = box
                    box.center_x = new_tile.center_x
                    box.center_y = new_tile.center_y
                    self.player_x = new_x
                    self.player_y = new_y

    def check_win(self) -> bool:
        """ To win, all goals must be covered with boxes """
        goals = [t for t in self._grid if t[0] == TileType.GOAL and t[1].box_here == None]        
        return len(goals) == 0
