"""
Module: 'uasyncio.stream' on micropython-esp32-1.17
"""
# MCU: {'ver': '1.17', 'port': 'esp32', 'arch': 'xtensawin', 'sysname': 'esp32', 'release': '1.17.0', 'name': 'micropython', 'mpy': 10757, 'version': '1.17.0', 'machine': 'ESP32 module with ESP32', 'build': '', 'nodename': 'esp32', 'platform': 'esp32', 'family': 'micropython'}
# Stubber: 1.4.2
from typing import Any

# import core

class Stream:
    ''
    def __init__(self, *args) -> None:
        ...

    def close(self, *args) -> Any:
        ...

    read : Any ## <class 'generator'> = <generator>
    readinto : Any ## <class 'generator'> = <generator>
    readline : Any ## <class 'generator'> = <generator>
    def write(self, *args) -> Any:
        ...

    wait_closed : Any ## <class 'generator'> = <generator>
    aclose : Any ## <class 'generator'> = <generator>
    awrite : Any ## <class 'generator'> = <generator>
    awritestr : Any ## <class 'generator'> = <generator>
    def get_extra_info(self, *args) -> Any:
        ...

    readexactly : Any ## <class 'generator'> = <generator>
    drain : Any ## <class 'generator'> = <generator>

class StreamReader:
    ''
    def __init__(self, *args) -> None:
        ...

    def close(self, *args) -> Any:
        ...

    read : Any ## <class 'generator'> = <generator>
    readinto : Any ## <class 'generator'> = <generator>
    readline : Any ## <class 'generator'> = <generator>
    def write(self, *args) -> Any:
        ...

    wait_closed : Any ## <class 'generator'> = <generator>
    aclose : Any ## <class 'generator'> = <generator>
    awrite : Any ## <class 'generator'> = <generator>
    awritestr : Any ## <class 'generator'> = <generator>
    def get_extra_info(self, *args) -> Any:
        ...

    readexactly : Any ## <class 'generator'> = <generator>
    drain : Any ## <class 'generator'> = <generator>

class StreamWriter:
    ''
    def __init__(self, *args) -> None:
        ...

    def close(self, *args) -> Any:
        ...

    read : Any ## <class 'generator'> = <generator>
    readinto : Any ## <class 'generator'> = <generator>
    readline : Any ## <class 'generator'> = <generator>
    def write(self, *args) -> Any:
        ...

    wait_closed : Any ## <class 'generator'> = <generator>
    aclose : Any ## <class 'generator'> = <generator>
    awrite : Any ## <class 'generator'> = <generator>
    awritestr : Any ## <class 'generator'> = <generator>
    def get_extra_info(self, *args) -> Any:
        ...

    readexactly : Any ## <class 'generator'> = <generator>
    drain : Any ## <class 'generator'> = <generator>
open_connection : Any ## <class 'generator'> = <generator>

class Server:
    ''
    def close(self, *args) -> Any:
        ...

    wait_closed : Any ## <class 'generator'> = <generator>
start_server : Any ## <class 'generator'> = <generator>
stream_awrite : Any ## <class 'generator'> = <generator>
