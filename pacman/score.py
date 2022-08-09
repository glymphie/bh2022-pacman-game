import displayio
import terminalio
import adafruit_imageload
import adafruit_display_text
from general import transparency

class Score:
    '''Keeps track of score
    '''

    transparent_color = 0xFF00FF
    highscore: int = 0
    cheese_score: int = 10
    super_cheese_score: int = 100
    eat_ghost_score: int = 200
    cherry_score: int = 500
    strawberry_score: int = 1000
    bitcoin_count: int = 0

    def __init__(self, sprite_sheet) -> None:
        self.score_group = displayio.Group(scale=1)

        bitmap, palette = adafruit_imageload.load(
            sprite_sheet,
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )

        self.highscore_sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width = 6,
            height = 1,
            tile_width = 8,
            tile_height = 10,
        )

        self.bitcoinscore_sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width = 6,
            height = 1,
            tile_width = 8,
            tile_height = 10,
        )

        for x in range(6):
            self.bitcoinscore_sprite[x] = x
        self.bitcoinscore_sprite.x = 127 - 6*8

        transparency.make_shader_transparent(self.highscore_sprite.pixel_shader, palette)
        transparency.make_shader_transparent(self.bitcoinscore_sprite.pixel_shader, palette)

        for x in range(6):
            self.highscore_sprite[x] = x

        self.highscore_area = adafruit_display_text.label.Label(terminalio.FONT, text='0' + ' '*10 , color=0xFFFFFF)
        self.highscore_area.x = 3
        self.highscore_area.y = 5
        self.highscore_area.anchor_point = (1.0, 0.5)

        self.bitcoinscore_area = adafruit_display_text.label.Label(terminalio.FONT, text='0' + ' '*3, color=0xf2ff00)
        self.bitcoinscore_area.x = 107
        self.bitcoinscore_area.y = 5
        self.bitcoinscore_area.anchor_point = (1.0, 0.5)

        self.score_group.append(self.highscore_sprite)
        self.score_group.append(self.bitcoinscore_sprite)
        self.score_group.append(self.highscore_area)
        self.score_group.append(self.bitcoinscore_area)

    def add_score(self, type_of_sprite):
        self.highscore += type_of_sprite
        self._update_score()

    def _update_score(self):
        self.highscore_area.text = str(self.highscore)

    def add_bitcoin(self):
        self.bitcoin_count += 1
        self.bitcoinscore_area.text = str(self.highscore)

