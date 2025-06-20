# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-FileCopyrightText: Adapted from Phil B.'s 16bit_hello Arduino Code
#
# SPDX-License-Identifier: MIT

import gc
import math
from random import randint
import time
import displayio
import picodvi
import board
import framebufferio
import vectorio
import terminalio
import simpleio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
import thermometer

# check for DVI Feather with built-in display
if 'DISPLAY' in dir(board):
    display = board.DISPLAY

# check for DVI feather without built-in display
elif 'CKP' in dir(board):
    displayio.release_displays()
    fb = picodvi.Framebuffer(320, 240,
        clk_dp=board.CKP, clk_dn=board.CKN,
        red_dp=board.D0P, red_dn=board.D0N,
        green_dp=board.D1P, green_dn=board.D1N,
        blue_dp=board.D2P, blue_dn=board.D2N,
        color_depth=8)
    display = framebufferio.FramebufferDisplay(fb)
# otherwise assume Pico
else:
    displayio.release_displays()
    fb = picodvi.Framebuffer(320, 240,
        clk_dp=board.GP12, clk_dn=board.GP13,
        red_dp=board.GP10, red_dn=board.GP11,
        green_dp=board.GP8, green_dn=board.GP9,
        blue_dp=board.GP6, blue_dn=board.GP7,
        color_depth=8)
    display = framebufferio.FramebufferDisplay(fb)

bitmap = displayio.Bitmap(display.width, display.height, 3)

red = 0xff0000
yellow = 0xcccc00
orange = 0xff5500
blue = 0x0000ff
pink = 0xff00ff
purple = 0x5500ff
white = 0xffffff
green =  0x00ff00
aqua = 0x125690

palette = displayio.Palette(3)
palette[0] = 0x000000 # black
palette[1] = white
palette[2] = yellow

palette.make_transparent(0)

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()

def clean_up(group_name):
    for _ in range(len(group_name)):
        group_name.pop()
    gc.collect()

def show_temperature(my_font, temperature):
    gc.collect()
    text_area = label.Label(my_font, text=temperature, color=white)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (display.width / 2, display.height / 2)
    group.append(text_area)
    return group

def show_image():
    gc.collect()
    blinka_bitmap = displayio.OnDiskBitmap("/logo.bmp")
    blinka_grid = displayio.TileGrid(blinka_bitmap, pixel_shader=blinka_bitmap.pixel_shader)
    gc.collect()
    group.append(blinka_grid)

    del blinka_grid
    del blinka_bitmap
    gc.collect()
    return group
    

display.root_group = group

group = show_image()
time.sleep(5)
#my_font = bitmap_font.load_font("/SevenSegmentRegular-82.bdf")
#my_font = bitmap_font.load_font("/SevenSegmentMirrored-82.bdf")
#my_font = bitmap_font.load_font("/SevenSegmentMirroredFlipped-82.bdf")
my_font = bitmap_font.load_font("/SevenSegmentMirroredAndFlipped-82.bdf")
while True:
    temperature = thermometer.current()
    #temperature = ''.join([c for c in temperature][::-1])
    #print(temperature)
    clean_up(group)
    group = show_temperature(my_font, temperature)
    time.sleep(5)  

del my_font
gc.collect()

