from typing import Any

class Color:
    def _available() -> None: ...
    def _read_u16() -> None: ...
    def _read_u8() -> None: ...
    def _register_char() -> None: ...
    def _register_short() -> None: ...
    def _valid() -> None: ...
    def _write_u16() -> None: ...
    def _write_u8() -> None: ...
    blue: Any
    def deinit() -> None: ...
    def enable() -> None: ...
    def getRGB() -> None: ...
    green: Any
    portMethod: int
    rawData: Any
    red: Any
    def setGains() -> None: ...
    def setIntegrationTime() -> None: ...

INT_TIME_DELAY: Any
_CYCLES: Any
_GAINS: Any
_INTEGRATION_TIME_THRESHOLD_HIGH: float
_INTEGRATION_TIME_THRESHOLD_LOW: float

def const() -> None: ...

i2c_bus: Any
time: Any
unit: Any
ustruct: Any