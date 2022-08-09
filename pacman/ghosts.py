import random
import displayio
import adafruit_imageload
from general import transparency


class Ghost:
    '''Ghost characters class with sprite sheet

       Tiles: 13 x 13
       1st: 0 = left, 1 = up, 2 = right, 3 = down
       vuln 1: 4
       vuln 2: 5
       dead:   6
       None:   7
    '''

    direction_left: int = 0
    direction_up: int = 1
    direction_right: int = 2
    direction_down: int = 3
    vuln1 = 4
    vuln2 = 5
    dead = 6
    no_sprite = 7
    sprite_size = 13
    move_counter = 0
    alive = True
    dead_counter = 0

    def __init__(self, sprite_sheet: str, chosen_map, pacman_himself, highscore, screen_width: int, screen_height: int, direction: int, x_pos: int, y_pos: int, speed: int):
        bitmap, palette = adafruit_imageload.load(
            sprite_sheet,
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )

        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width = 1,
            height = 1,
            tile_width = self.sprite_size,
            tile_height = self.sprite_size,
        )

        self.WIDTH = screen_width
        self.HEIGHT = screen_height

        self.direction: int = direction # Initial direction
        self.x_original = x_pos
        self.y_original = y_pos
        self.x_position = x_pos
        self.y_position = y_pos
        self.speed = speed
        self.chosen_map = chosen_map
        self.highscore = highscore
        self.pacman_himself = pacman_himself
        self.sprite.x = self.x_position
        self.sprite.y = self.y_position
        self.sprite[0] = self.direction

        transparency.make_shader_transparent(self.sprite.pixel_shader, palette)

    @property
    def sprite_front(self):
        if self.direction == self.direction_left:
            return list(zip([self.x_position - 2] * self.sprite_size, range(self.y_position, self.y_position + self.sprite_size)))
        elif self.direction == self.direction_right:
            return list(zip([self.x_position + self.sprite_size + 1] * self.sprite_size, range(self.y_position, self.y_position + self.sprite_size)))
        elif self.direction == self.direction_up:
            return list(zip(range(self.x_position, self.x_position + self.sprite_size), [self.y_position - 2] * self.sprite_size))
        elif self.direction == self.direction_down:
            return list(zip(range(self.x_position, self.x_position + self.sprite_size), [self.y_position + self.sprite_size + 1] * self.sprite_size))

    @property
    def sprite_center(self):
        center_points = []
        for x in range(5,9):
            for y in range(5,9):
                center_points.append((self.x_position + x, self.y_position + y))
        return center_points

    def move(self):
        chosen_way = self._choose_way()
        self._get_direction(chosen_way)
        self._limit_movement()
        self._update_position()
        self._set_position()
        self._update_sprite()
        self.speed = 1

    def _choose_way(self):
        for front in self.sprite_front:
            if self.chosen_map.bitmap[front[0], front[1]] == 1:
                self.move_counter = 0
                return self._random_direction()

        if self.move_counter == 15:
            self.move_counter = 0
            return self._random_direction()

        self.move_counter += 1
        return self.direction

    def _random_direction(self):
        return random.randint(0, 3)

    def _get_direction(self, chosen_way):
        self.direction = chosen_way

    def _update_position(self):
        if self.direction == self.direction_left:
            self.x_position -= self.speed
        elif self.direction == self.direction_right:
            self.x_position += self.speed
        elif self.direction == self.direction_up:
            self.y_position -= self.speed
        elif self.direction == self.direction_down:
            self.y_position += self.speed

    def _limit_movement(self):
        for front in self.sprite_front:
            if front[0] < 0 or front[0] > self.WIDTH - 1:
                self.speed = -self.WIDTH + self.sprite_size + 1
            elif front[1] < 0 or front[1] > self.HEIGHT - 1:
                self.speed = -self.HEIGHT + self.sprite_size + 1
            elif self.chosen_map.bitmap[front[0], front[1]] == 1:
                self.speed = 0

    def _set_position(self):
        self.sprite.x = self.x_position
        self.sprite.y = self.y_position

    def _update_sprite(self):
        if not self.alive:
            self.dead_counter += 1
            if self.dead_counter < 50:
                self.sprite[0] = 6
                return
            elif self.dead_counter == 400:
                self.alive = True
                self.x_position = self.x_original
                self.y_position = self.y_original
                self.dead_counter = 0
                return
            self.sprite[0] = 7
        elif self.pacman_himself.invinsible:
            if self.pacman_himself.invinsible_counter > 160 and self.pacman_himself.invinsible_counter % 2 == 0 :
                self.sprite[0] = 5
                return
            self.sprite[0] = 4
        else:
            self.sprite[0] = self.direction

    def check_collision(self):
        collision = self.pacman_himself.check_pacman_and_ghost_collision(self)
        if self.pacman_himself.invinsible and collision and self.alive:
            self.alive = False
            self.highscore.add_score(self.highscore.eat_ghost_score)
        elif collision and self.alive:
            return True
        return False
