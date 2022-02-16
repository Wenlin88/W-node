from typing import Any

HEAP_DATA: int
HEAP_EXEC: int

class NVS:
    def __init__(self, *argv, **kwargs) -> None: ...
    def commit(self, *args, **kwargs) -> Any: ...
    def erase_key(self, *args, **kwargs) -> Any: ...
    def get_blob(self, *args, **kwargs) -> Any: ...
    def get_i32(self, *args, **kwargs) -> Any: ...
    def set_blob(self, *args, **kwargs) -> Any: ...
    def set_i32(self, *args, **kwargs) -> Any: ...

class Partition:
    def __init__(self, *argv, **kwargs) -> None: ...
    def find(self, *args, **kwargs) -> Any: ...
    BOOT: int
    RUNNING: int
    TYPE_APP: int
    TYPE_DATA: int
    def get_next_update(self, *args, **kwargs) -> Any: ...
    def info(self, *args, **kwargs) -> Any: ...
    def ioctl(self, *args, **kwargs) -> Any: ...
    @classmethod
    def mark_app_valid_cancel_rollback(cls, *args, **kwargs) -> Any: ...
    def readblocks(self, *args, **kwargs) -> Any: ...
    def set_boot(self, *args, **kwargs) -> Any: ...
    def writeblocks(self, *args, **kwargs) -> Any: ...

class RMT:
    def __init__(self, *argv, **kwargs) -> None: ...
    def bitstream_channel(self, *args, **kwargs) -> Any: ...
    def clock_div(self, *args, **kwargs) -> Any: ...
    def deinit(self, *args, **kwargs) -> Any: ...
    def loop(self, *args, **kwargs) -> Any: ...
    def source_freq(self, *args, **kwargs) -> Any: ...
    def wait_done(self, *args, **kwargs) -> Any: ...
    def write_pulses(self, *args, **kwargs) -> Any: ...

class ULP:
    def __init__(self, *argv, **kwargs) -> None: ...
    RESERVE_MEM: int
    def load_binary(self, *args, **kwargs) -> Any: ...
    def run(self, *args, **kwargs) -> Any: ...
    def set_wakeup_period(self, *args, **kwargs) -> Any: ...

WAKEUP_ALL_LOW: bool
WAKEUP_ANY_HIGH: bool

def hall_sensor(*args, **kwargs) -> Any: ...
def idf_heap_info(*args, **kwargs) -> Any: ...
def raw_temperature(*args, **kwargs) -> Any: ...
def wake_on_ext0(*args, **kwargs) -> Any: ...
def wake_on_ext1(*args, **kwargs) -> Any: ...
def wake_on_touch(*args, **kwargs) -> Any: ...
