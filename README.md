# Game Development with Python

This is information and example code written for a talk I did at
the Greenville Python Meetup in May of 2019.

## Examples

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

#### Further Ideas

- Animation
- Level Collection selection menu (perhaps with Tk?)
- Level selection menu
- Alert player when game is no longer winnable
- Mouse-based controls
- "Undo" last move feature
- Show level collection name and level number in UI
- Save completion information (best times, moves, etc.)

## A Quick Intro to the Arcade Library

