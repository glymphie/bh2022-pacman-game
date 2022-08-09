import time
print("Hello, I'm alive!")
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""

import os

import board
import terminalio
import displayio
import digitalio
import pwmio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
from adafruit_slideshow import PlayBackOrder, SlideShow

def join(*xs):
    return '/'.join(x.rstrip('/') for x in xs)


def isfile(path):
    try:
        with open(path):
            pass
    except FileNotFoundError:
        return False
    else:
        return True

BTN_A = digitalio.DigitalInOut(board.BTN_A)
BTN_A.switch_to_input(pull=digitalio.Pull.UP)

BTN_B = digitalio.DigitalInOut(board.BTN_B)
BTN_B.switch_to_input(pull=digitalio.Pull.UP)

BTN_X = digitalio.DigitalInOut(board.BTN_X)
BTN_X.switch_to_input(pull=digitalio.Pull.UP)

BTN_Y = digitalio.DigitalInOut(board.BTN_Y)
BTN_Y.switch_to_input(pull=digitalio.Pull.UP)

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.CS
tft_dc = board.D1

display_bus = displayio.FourWire(
	spi, command=tft_dc, chip_select=tft_cs, reset=board.D0
)

WIDTH = 128
HEIGHT = 160

display = ST7735R(display_bus, width=WIDTH, height=HEIGHT, rotation=0, bgr=True, colstart=2, rowstart=1)

# bl = digitalio.DigitalInOut(board.PWM0)
# bl.direction = digitalio.Direction.OUTPUT
# bl.value = True

bl = pwmio.PWMOut(board.PWM0, frequency=5000, duty_cycle=0)
bl.duty_cycle = 60000

def DrawMenu(currentselected, paths):
    it = 0
    for opt in paths:
        it+=1

        menu_text0_group = displayio.Group(scale=1, x=8, y=10*it)
        if currentselected == it:
            menu_text0_area = label.Label(terminalio.FONT, text=opt, color=0xFFFFFF)
        else:
            menu_text0_area = label.Label(terminalio.FONT, text=opt, color=0x777777)
        menu_text0_group.append(menu_text0_area)
        menu.append(menu_text0_group)

    display.show(menu)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Create the slideshow object that plays through once alphabetically.
slideshow = SlideShow(display,
                      folder="/images",
                      loop=True,
                      order=PlayBackOrder.ALPHABETICAL,
                      dwell=0.5)
i=0

while slideshow.update():
    i+=1
    if i < 2:
        pass
    else:
        display.show(splash)
        time.sleep(0.2)
        break
    time.sleep(0.5)

selected = 1

dir_path = r'apps/'

del splash
# list to store files
res = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if isfile(join(dir_path, path)):
        res.append(path)

menu = displayio.Group()
DrawMenu(selected, res)
del menu

while True:
    if BTN_A.value == False:
        if selected == 1:
            pass
        else:
            menu = displayio.Group()
            selected-=1
            DrawMenu(selected, res)
            del menu
        time.sleep(0.3)

    if BTN_B.value == False:
        if selected == len(res):
            pass
        else:
            menu = displayio.Group()
            selected+=1
            DrawMenu(selected, res)
            del menu
        time.sleep(0.3)

    if BTN_X.value == False or BTN_Y.value == False:
        try:
            exec(open(join(dir_path, res[selected-1])).read())
        except:
            pass
        menu = displayio.Group()
        DrawMenu(selected, res)
        del menu
    pass
