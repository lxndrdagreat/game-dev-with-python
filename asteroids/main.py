import arcade
import math
from player import PlayerShip
from utils import ThemeColors
from bullet import Bullet
from typing import List
from asteroid import Asteroid, AsteroidSize
import random


class AsteroidsGame(arcade.Window):

    def __init__(self):
        # set up the window with size and title
        super().__init__(800, 600, 'Asteroids')

        # set the background color
        arcade.set_background_color(ThemeColors.BACKGROUND.color)

        # The player object
        self.player_ship = PlayerShip(400, 300)

        # active bullets
        self.bullets: List[Bullet] = []

        # asteroids
        self.asteroids: List[Asteroid] = []

        # input states
        self.input = {
            arcade.key.LEFT: False,
            arcade.key.RIGHT: False,
            arcade.key.UP: False,
            arcade.key.DOWN: False,
            arcade.key.SPACE: False
        }
        self.last_frame = 1
        self.spawn_asteroids()

    def spawn_asteroids(self):
        w, h = self.get_size()
        center_x = w / 2
        center_y = h / 2
        spawn_radius = w * 0.35

        for i in range(0, 5):
            angle = round(math.radians(random.randint(0, 360)), 2)
            offset_x = math.sin(angle) * spawn_radius
            offset_y = math.cos(angle) * spawn_radius
            spawn_x = center_x + offset_x
            spawn_y = center_y + offset_y
            new_asteroid = Asteroid(spawn_x, spawn_y, AsteroidSize.LARGE)
            self.asteroids.append(new_asteroid)

    def on_draw(self):
        """ Handle drawing here. """
        arcade.start_render()

        # draw player if alive
        if self.player_ship.alive:
            self.player_ship.draw()

        # draw bullets
        for bullet in self.bullets:
            bullet.draw()

        # draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw()

        # draw framerate in bottom-left corner
        arcade.draw_text(f'FPS: {round(1.0 / self.last_frame, 1)}', 5, 5, arcade.color.BLACK, 12)

    def on_update(self, delta):
        self.last_frame = delta
        screen_width, screen_height = self.get_size()

        # only update the player ship if it is alive
        if self.player_ship.alive:
            # apply user movement input
            if self.input[arcade.key.LEFT]:
                self.player_ship.add_rotation(1, delta)
            if self.input[arcade.key.RIGHT]:
                self.player_ship.add_rotation(-1, delta)
            if self.input[arcade.key.UP]:
                self.player_ship.add_acceleration()
            
            # update player cooldowns
            self.player_ship.update(delta)

            # if the player has asked to fire and can, then create a bullet:
            if self.input[arcade.key.SPACE] and self.player_ship.fire():
                b = Bullet((self.player_ship.x, self.player_ship.y), self.player_ship.rotation)
                self.bullets.append(b)

            # apply ship movement
            self.player_ship.apply_velocity(delta)

            # keep the ship on the screen
            if self.player_ship.x < 0:
                self.player_ship.x = screen_width
            elif self.player_ship.x > screen_width:
                self.player_ship.x = 0
            if self.player_ship.y < 0:
                self.player_ship.y = screen_height
            elif self.player_ship.y > screen_height:
                self.player_ship.y = 0

        # update bullets and remove dead ones
        for bullet in self.bullets:
            bullet.update(delta)
        self.bullets = [bullet for bullet in self.bullets if bullet.alive]

        # update asteroids
        for asteroid in self.asteroids:
            asteroid.update(delta, screen_width, screen_height)
            # handle collisions with bullets
            for bullet in self.bullets:
                if not bullet.alive:
                    continue
                # TODO: narrow down this loop based on distance from asteroid
                if asteroid.collides_with_point(bullet.x, bullet.y):
                    bullet.alive = False
                    asteroid.alive = False
                    if asteroid.size != AsteroidSize.SMALL:
                        for i in range(0, 3):
                            smaller_asteroid = Asteroid(asteroid.x, asteroid.y, AsteroidSize(asteroid.size - 1))
                            self.asteroids.append(smaller_asteroid)
                    break
            
            if not asteroid.alive:
                continue
            
            # check each of the player ships's points for intersection with the asteroid
            if self.player_ship.alive:
                for ship_point in self.player_ship.rotated_points():
                    if asteroid.collides_with_point(ship_point[0], ship_point[1]):
                        asteroid.alive = False
                        # TODO: handle player lives
                        self.player_ship.alive = False
                        break


        self.asteroids = [asteroid for asteroid in self.asteroids if asteroid.alive]

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # kill the game
            arcade.close_window()

        # apply input
        if key in self.input:
            self.input[key] = True

    def on_key_release(self, key, modifiers):
        if key in self.input:
            self.input[key] = False


if __name__ == '__main__':

    game = AsteroidsGame()
    arcade.run()
