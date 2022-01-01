"""
Module: 'upip_utarfile' on micropython-esp32-1.17
"""
# MCU: {'ver': '1.17', 'port': 'esp32', 'arch': 'xtensawin', 'sysname': 'esp32', 'release': '1.17.0', 'name': 'micropython', 'mpy': 10757, 'version': '1.17.0', 'machine': 'ESP32 module (spiram) with ESP32', 'build': '', 'nodename': 'esp32', 'platform': 'esp32', 'family': 'micropython'}
# Stubber: 1.4.2
from typing import Any

# import uctypes
DIRTYPE = 'dir' # type: str

class TarFile:
    ''
    def __init__(self, *args) -> None:
        ...

    def next(self, *args) -> Any:
        ...

    def extractfile(self, *args) -> Any:
        ...

TAR_HEADER = {} # type: dict
REGTYPE = 'file' # type: str
def roundup(*args) -> Any:
    ...


class FileSection:
    ''
    def __init__(self, *args) -> None:
        ...

    def read(self, *args) -> Any:
        ...

    def readinto(self, *args) -> Any:
        ...

    def skip(self, *args) -> Any:
        ...


class TarInfo:
    ''
