import displayio
import adafruit_imageload
from general import transparency


class Cheese:
    '''Logic of cheese and big cheese
    '''

    sprite_size = 8
    space_cheese = 0
    space_super_cheese = 1
    space_bitcoin = 2
    space_cherry = 3
    space_strawberry = 4
    space_empty = 5
    cheese_counter = 0
    victory_condition = 0


    def __init__(self, sprite_sheet: str, pacman_himself, highscore, cheese_map):
        bitmap, palette = adafruit_imageload.load(
            sprite_sheet,
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )

        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width = 16,
            height = 20,
            tile_width = self.sprite_size,
            tile_height = self.sprite_size,
        )

        self.pacman_himself = pacman_himself
        self.highscore = highscore

        self.cheese_map = cheese_map
        for line_num, line in enumerate(self.cheese_map):
            for grid_num, grid in enumerate(line):
                self.sprite[grid_num, line_num] = grid

        for line in self.cheese_map:
            self.victory_condition += line.count(0) + line.count(1)

        transparency.make_shader_transparent(self.sprite.pixel_shader, palette)

    def _check_sprite(self, sprite_value: int):
        for point in self.pacman_himself.sprite_center:
            pacman_eat_x = point[0] // self.sprite_size
            pacman_eat_y = point[1] // self.sprite_size
            if self.sprite[pacman_eat_x, pacman_eat_y] == sprite_value:
                self.sprite[pacman_eat_x, pacman_eat_y] = 5
                return True
        return False

    def update(self):
        self.check_cheese()
        self.check_super_cheese()

    def check_cheese(self):
        if self._check_sprite(self.space_cheese):
            self.highscore.add_score(self.highscore.cheese_score)
            self.cheese_counter += 1

    def check_super_cheese(self):
        if self._check_sprite(self.space_super_cheese):
            self.highscore.add_score(self.highscore.super_cheese_score)
            self.cheese_counter += 1
            self.pacman_himself.invinsible = True
            self.pacman_himself.invinsible_counter = 0

    def check_victory(self):
        if self.cheese_counter == self.victory_condition:
            return True

