"""
Module: 'ds18x20' on micropython-esp32-1.17
"""
# MCU: {'ver': '1.17', 'port': 'esp32', 'arch': 'xtensawin', 'sysname': 'esp32', 'release': '1.17.0', 'name': 'micropython', 'mpy': 10757, 'version': '1.17.0', 'machine': 'ESP32 module (spiram) with ESP32', 'build': '', 'nodename': 'esp32', 'platform': 'esp32', 'family': 'micropython'}
# Stubber: 1.4.2
from typing import Any

def const(*args) -> Any:
    ...


class DS18X20:
    ''
    def __init__(self, *args) -> None:
        ...

    def scan(self, *args) -> Any:
        ...

    def convert_temp(self, *args) -> Any:
        ...

    def read_scratch(self, *args) -> Any:
        ...

    def write_scratch(self, *args) -> Any:
        ...

    def read_temp(self, *args) -> Any:
        ...

