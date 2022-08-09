import time
import displayio
import adafruit_imageload
from general import transparency


class PacmanHimself:
    '''Pacman character class with sprite sheet

       Tiles: 13 x 13
       0 = left, 1 = up, 2 = right, 3 = down, 4 = closed
    '''

    pacman_direction_left: int = 0
    pacman_direction_up: int = 1
    pacman_direction_right: int = 2
    pacman_direction_down: int = 3
    pacman_direction_closed: int = 4
    pacman_direction: int = pacman_direction_down # Initial direction
    pacman_x_position: int = 128//2-7 # Initial positions
    pacman_y_position: int = 7
    pacman_speed: int = 1
    update_counter: int = 0
    sprite_size: int = 13
    invinsible: bool = False
    invinsible_counter: int = 0
    alive: bool = True


    def __init__(self, sprite_sheet: str, chosen_map, screen_width: int, screen_height: int):
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

        self.chosen_map = chosen_map

        self.sprite.x = self.pacman_x_position
        self.sprite.y = self.pacman_y_position
        self.sprite[0] = self.pacman_direction

        transparency.make_shader_transparent(self.sprite.pixel_shader, palette)

    @property
    def sprite_front(self):
        if self.pacman_direction == self.pacman_direction_left:
            return list(zip([self.pacman_x_position - 2] * self.sprite_size, range(self.pacman_y_position, self.pacman_y_position + self.sprite_size)))
        elif self.pacman_direction == self.pacman_direction_right:
            return list(zip([self.pacman_x_position + self.sprite_size + 1] * self.sprite_size, range(self.pacman_y_position, self.pacman_y_position + self.sprite_size)))
        elif self.pacman_direction == self.pacman_direction_up:
            return list(zip(range(self.pacman_x_position, self.pacman_x_position + self.sprite_size), [self.pacman_y_position - 2] * self.sprite_size))
        elif self.pacman_direction == self.pacman_direction_down:
            return list(zip(range(self.pacman_x_position, self.pacman_x_position + self.sprite_size), [self.pacman_y_position + self.sprite_size + 1] * self.sprite_size))

    @property
    def sprite_center(self):
        point1 = (self.pacman_x_position + 5, self.pacman_y_position + 5)
        point2 = (self.pacman_x_position + 8, self.pacman_y_position + 5)
        point3 = (self.pacman_x_position + 5, self.pacman_y_position + 8)
        point4 = (self.pacman_x_position + 8, self.pacman_y_position + 8)
        return (point1, point2, point3, point4)

    def move(self, button_value: int):
        self._get_direction(button_value)
        self._limit_movement()
        self._update_position()
        self._set_position()
        self._invinsible()
        if self.update_counter == 2:
            self._update_sprite()
            self.update_counter = 0
        self.update_counter += 1
        self.pacman_speed = 1

    def _invinsible(self):
        if self.invinsible:
            self.invinsible_counter += 1
            if self.invinsible_counter == 200:
                self.invinsible = False

    def _get_direction(self, button_value: int):
        if button_value < 4:
            self.pacman_direction = button_value

    def _update_position(self):
        if self.pacman_direction == self.pacman_direction_left:
            self.pacman_x_position -= self.pacman_speed
        elif self.pacman_direction == self.pacman_direction_right:
            self.pacman_x_position += self.pacman_speed
        elif self.pacman_direction == self.pacman_direction_up:
            self.pacman_y_position -= self.pacman_speed
        elif self.pacman_direction == self.pacman_direction_down:
            self.pacman_y_position += self.pacman_speed

    def _limit_movement(self):
        for front in self.sprite_front:
            if front[0] < 0 or front[0] > self.WIDTH - 1:
                self.pacman_speed = -self.WIDTH + self.sprite_size + 1
            elif front[1] < 0 or front[1] > self.HEIGHT - 1:
                self.pacman_speed = -self.HEIGHT + self.sprite_size + 1
            elif self.chosen_map.bitmap[front[0], front[1]] == 1:
                self.pacman_speed = 0

    def _set_position(self):
        self.sprite.x = self.pacman_x_position
        self.sprite.y = self.pacman_y_position

    def _update_sprite(self):
        if self.sprite[0] != self.pacman_direction_closed:
            self.sprite[0] = self.pacman_direction_closed
        else:
            self.sprite[0] = self.pacman_direction

    def check_pacman_and_ghost_collision(self, ghost):
        for pacman_point in self.sprite_center:
            for ghost_point in ghost.sprite_center:
                if pacman_point == ghost_point:
                    return True

    def dead(self):
        for x in range(5,14):
            self.sprite[0] = x
            time.sleep(0.1)

        self.alive = False

