import time
import displayio
import adafruit_imageload
from general import transparency

class Announcer:
    def __init__(self, sprite_sheet) -> None:
        self.group = displayio.Group(scale=1)

        bitmap, palette = adafruit_imageload.load(
            sprite_sheet,
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )

        self.ready_sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width = 1,
            height = 1,
            tile_width = 40,
            tile_height = 13,
        )

        self.victory_sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width = 1,
            height = 1,
            tile_width = 40,
            tile_height = 13,
        )

        self.dead_sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width = 1,
            height = 1,
            tile_width = 40,
            tile_height = 13,
        )

        self.victory_sprite[0] = 0
        self.ready_sprite[0] = 1
        self.dead_sprite[0] = 2

        self.ready_sprite.x = 128 // 2 - 20 - 1
        self.ready_sprite.y = 160 // 2 - 7 - 1
        self.dead_sprite.x = 128 // 2 - 20 - 1
        self.dead_sprite.y = 160 // 2 - 7 - 1
        self.victory_sprite.x = 128 // 2 - 20
        self.victory_sprite.y = 160 // 2 - 7

        transparency.make_shader_transparent(self.ready_sprite.pixel_shader, palette)
        transparency.make_shader_transparent(self.dead_sprite.pixel_shader, palette)
        transparency.make_shader_transparent(self.victory_sprite.pixel_shader, palette)

    def start(self):
        self.group.append(self.ready_sprite)
        time.sleep(3)
        self.group.pop()

    def dead(self):
        self.group.append(self.dead_sprite)
        time.sleep(3)
        self.group.pop()

    def victory(self):
        self.group.append(self.victory_sprite)
        time.sleep(3)
        self.group.pop()
