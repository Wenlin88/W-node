"""
Module: 'umqtt.simple' on micropython-esp32-1.17
"""
# MCU: {'ver': '1.17', 'port': 'esp32', 'arch': 'xtensawin', 'sysname': 'esp32', 'release': '1.17.0', 'name': 'micropython', 'mpy': 10757, 'version': '1.17.0', 'machine': 'ESP32 module (spiram) with ESP32', 'build': '', 'nodename': 'esp32', 'platform': 'esp32', 'family': 'micropython'}
# Stubber: 1.4.2
from typing import Any

def hexlify(*args) -> Any:
    ...

# import socket
# import struct

class MQTTException:
    ''

class MQTTClient:
    ''
    def __init__(self, *args) -> None:
        ...

    def connect(self, *args) -> Any:
        ...

    def disconnect(self, *args) -> Any:
        ...

    def set_callback(self, *args) -> Any:
        ...

    def set_last_will(self, *args) -> Any:
        ...

    def ping(self, *args) -> Any:
        ...

    def publish(self, *args) -> Any:
        ...

    def subscribe(self, *args) -> Any:
        ...

    def wait_msg(self, *args) -> Any:
        ...

    def check_msg(self, *args) -> Any:
        ...

