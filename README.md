# Game Development with Python

This is information and example code written for a talk I did at
the Greenville Python Meetup in May of 2019.

[Google Presentation](https://docs.google.com/presentation/d/1rTE7dVM-Q9OxJkT1uTwN7Yr7UDV6ImvAkB11DylUKkk/edit?usp=sharing)
for the talk.

## Arcade Examples

These example games all use [Arcade](http://arcade.academy/) which can
be installed via `pip install arcade`.

### Asteroids

A basic version of Asteroids, this game showcases some basics of the Arcade
library like subclassing the `Window` class, keyboard input handling and
drawing basic shapes.

#### Further Ideas

- Sound
- Player max speed
- Enemy ships
- Wrap bullets when they go off screen (like the player ship does)
- Use sprites instead of shapes
- Player lives
- Glorious explosion when player ship explodes
- Keep score
- "Game Over" handling
- Game menus and make it so you can start a new game without re-running the app
- Optimize drawing requests

### Minesweeper

Shows mouse interaction, text drawing, and using sprites for drawing.

#### Further Ideas

- UI to select difficulty
- Allow resizing the window

### Sokoban

- [About Sokoban](https://en.wikipedia.org/wiki/Sokoban)
- [Level format](http://www.sokobano.de/wiki/index.php?title=Level_format)
- [Level packs](http://www.sourcecode.se/sokoban/levels)

Arrow keys to move. `F2` to restart the current level. `F3` to skip
to the next level.

#### Further Ideas

- Animation
- Level Collection selection menu (perhaps with Tk?)
- Level selection menu
- Alert player when game is no longer winnable
- Mouse-based controls
- "Undo" last move feature
- Show level collection name and level number in UI
- Save completion information (best times, moves, etc.)

## Resource Links

- [Py-SDL2](https://github.com/marcusva/py-sdl2)
- [PySFML](https://github.com/Sonkun/python-sfml)
- [PyGLFW](https://github.com/FlorianRhiem/pyGLFW)
- [PyOpenGL](http://pyopengl.sourceforge.net/documentation/index.html)
- [Kivy](https://kivy.org/)
- [Kivent](https://github.com/kivy/kivent)
- [PyGame](https://www.pygame.org/news)
- [Pyglet](https://pyglet.readthedocs.io)
- [Arcade](http://arcade.academy/)
- [Arcade Book](https://arcade-book.readthedocs.io/en/latest/)
- [Ren’Py](https://www.renpy.org/)
- [Panda3D](https://www.panda3d.org/)
- [Pyxel](https://github.com/kitao/pyxel)
- [Python TCOD](https://github.com/libtcod/python-tcod)
- [Cocos2D](http://python.cocos2d.org/)
- [Open Game Art](https://opengameart.org/)
- [Free art by Kenney](https://www.kenney.nl/)
- [Free Game Icons](https://game-icons.net/)
