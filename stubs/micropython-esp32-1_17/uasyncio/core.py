"""
Module: 'uasyncio.core' on micropython-esp32-1.17
"""
# MCU: {'ver': '1.17', 'port': 'esp32', 'arch': 'xtensawin', 'sysname': 'esp32', 'release': '1.17.0', 'name': 'micropython', 'mpy': 10757, 'version': '1.17.0', 'machine': 'ESP32 module with ESP32', 'build': '', 'nodename': 'esp32', 'platform': 'esp32', 'family': 'micropython'}
# Stubber: 1.4.2
from typing import Any


class CancelledError:
    ''

class Task:
    ''

class TaskQueue:
    ''
    def remove(self, *args) -> Any:
        ...

    def peek(self, *args) -> Any:
        ...

    def pop_head(self, *args) -> Any:
        ...

    def push_head(self, *args) -> Any:
        ...

    def push_sorted(self, *args) -> Any:
        ...

def run(*args) -> Any:
    ...

# import select
def sleep(*args) -> Any:
    ...

def sleep_ms(*args) -> Any:
    ...

# import sys
def ticks_add(*args) -> Any:
    ...

def ticks_diff(*args) -> Any:
    ...

def ticks(*args) -> Any:
    ...


class TimeoutError:
    ''

class SingletonGenerator:
    ''
    def __init__(self, *args) -> None:
        ...


class IOQueue:
    ''
    def __init__(self, *args) -> None:
        ...

    def remove(self, *args) -> Any:
        ...

    def queue_read(self, *args) -> Any:
        ...

    def queue_write(self, *args) -> Any:
        ...

    def wait_io_event(self, *args) -> Any:
        ...

def create_task(*args) -> Any:
    ...

def run_until_complete(*args) -> Any:
    ...


class Loop:
    ''
    def close(self, *args) -> Any:
        ...

    def stop(self, *args) -> Any:
        ...

    def create_task(self, *args) -> Any:
        ...

    def run_until_complete(self, *args) -> Any:
        ...

    def call_exception_handler(self, *args) -> Any:
        ...

    def run_forever(self, *args) -> Any:
        ...

    def set_exception_handler(self, *args) -> Any:
        ...

    def get_exception_handler(self, *args) -> Any:
        ...

    def default_exception_handler(self, *args) -> Any:
        ...

def get_event_loop(*args) -> Any:
    ...

def current_task(*args) -> Any:
    ...

def new_event_loop(*args) -> Any:
    ...

