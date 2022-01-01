"""
ttgo_hello.py

    Writes "Hello!" in random colors at random locations on a
    LILYGO® TTGO T-Display.

    https://www.youtube.com/watch?v=atBa0BYPAAc

"""
import random
from machine import Pin, SoftSPI
import ttgo_display.st7789py as st7789

from ttgo_display.romfonts import vga1_16x32 as font

class display():
    def __init__(self):
        spi = SoftSPI(
            baudrate=20000000,
            polarity=1,
            phase=0,
            sck=Pin(18),
            mosi=Pin(19),
            miso=Pin(13))
        tft = st7789.ST7789(
            spi,
            135,
            240,
            reset=Pin(23, Pin.OUT),
            cs=Pin(5, Pin.OUT),
            dc=Pin(16, Pin.OUT),
            backlight=Pin(4, Pin.OUT),
            rotation=0)
        
        tft.rotation(0)
        tft.fill(0)
        self.tft = tft  
    def text(self, msg, row):
        self.tft.text(
            font,
            msg,
            0,
            (font.HEIGHT + 2) * row,
            st7789.color565(255, 255, 255),
            st7789.color565(0,0,0)
            )
