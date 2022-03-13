"""
Module: 'st7789' on micropython-v1.18-128-esp32
"""
# MCU: {'ver': 'v1.18-128', 'port': 'esp32', 'arch': 'xtensawin', 'sysname': 'esp32', 'release': '1.18.0', 'name': 'micropython', 'mpy': 10757, 'version': '1.18.0', 'machine': 'TTGO T-Display with ESP32', 'build': '128', 'nodename': 'esp32', 'platform': 'esp32', 'family': 'micropython'}
# Stubber: 1.5.5
from typing import Any

BGR = 8 # type: int
BLACK = 0 # type: int
BLUE = 31 # type: int
CYAN = 2047 # type: int
FAST = 0 # type: int
GREEN = 2016 # type: int
MADCTL_MH = 4 # type: int
MADCTL_ML = 16 # type: int
MADCTL_MV = 32 # type: int
MADCTL_MX = 64 # type: int
MADCTL_MY = 128 # type: int
MAGENTA = 63519 # type: int
RED = 63488 # type: int
RGB = 0 # type: int
SLOW = 1 # type: int

class ST7789():
    ''
    def __init__(self, *argv, **kwargs) -> None:
        ''
        ...
    def write(self, *args, **kwargs) -> Any:
        ...

    def bitmap(self, *args, **kwargs) -> Any:
        ...

    def blit_buffer(self, *args, **kwargs) -> Any:
        ...

    def bounding(self, *args, **kwargs) -> Any:
        ...

    def circle(self, *args, **kwargs) -> Any:
        ...

    def draw(self, *args, **kwargs) -> Any:
        ...

    def draw_len(self, *args, **kwargs) -> Any:
        ...

    def fill(self, *args, **kwargs) -> Any:
        ...

    def fill_circle(self, *args, **kwargs) -> Any:
        ...

    def fill_polygon(self, *args, **kwargs) -> Any:
        ...

    def fill_rect(self, *args, **kwargs) -> Any:
        ...

    def hard_reset(self, *args, **kwargs) -> Any:
        ...

    def height(self, *args, **kwargs) -> Any:
        ...

    def hline(self, *args, **kwargs) -> Any:
        ...

    def init(self, *args, **kwargs) -> Any:
        ...

    def inversion_mode(self, *args, **kwargs) -> Any:
        ...

    def jpg(self, *args, **kwargs) -> Any:
        ...

    def jpg_decode(self, *args, **kwargs) -> Any:
        ...

    def line(self, *args, **kwargs) -> Any:
        ...

    def madctl(self, *args, **kwargs) -> Any:
        ...

    def map_bitarray_to_rgb565(self, *args, **kwargs) -> Any:
        ...

    def off(self, *args, **kwargs) -> Any:
        ...

    def offset(self, *args, **kwargs) -> Any:
        ...

    def on(self, *args, **kwargs) -> Any:
        ...

    def pixel(self, *args, **kwargs) -> Any:
        ...

    def polygon(self, *args, **kwargs) -> Any:
        ...

    def polygon_center(self, *args, **kwargs) -> Any:
        ...

    def rect(self, *args, **kwargs) -> Any:
        ...

    def rotation(self, *args, **kwargs) -> Any:
        ...

    def sleep_mode(self, *args, **kwargs) -> Any:
        ...

    def soft_reset(self, *args, **kwargs) -> Any:
        ...

    def text(self, *args, **kwargs) -> Any:
        ...

    def vline(self, *args, **kwargs) -> Any:
        ...

    def vscrdef(self, *args, **kwargs) -> Any:
        ...

    def vscsad(self, *args, **kwargs) -> Any:
        ...

    def width(self, *args, **kwargs) -> Any:
        ...

    def write_len(self, *args, **kwargs) -> Any:
        ...

WHITE = 65535 # type: int
WRAP = 3 # type: int
WRAP_H = 2 # type: int
WRAP_V = 1 # type: int
YELLOW = 65504 # type: int
def color565(*args, **kwargs) -> Any:
    ...

def map_bitarray_to_rgb565(*args, **kwargs) -> Any:
    ...

