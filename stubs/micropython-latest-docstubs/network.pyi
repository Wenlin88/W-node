from typing import Any, List, Optional, Tuple, Union

class AbstractNIC:
    def __init__(self, id: Any | None = ..., *args) -> None: ...
    def active(self, is_active: Optional[Any]) -> None: ...
    def connect(self, service_id, key: Any | None = ..., *args: Optional[Any]) -> None: ...
    def disconnect(self) -> None: ...
    def isconnected(self) -> bool: ...
    def scan(self, *args) -> List[Tuple]: ...
    def status(self, param: Optional[Any]) -> Any: ...
    def ifconfig(self, configtuple: Optional[Any]) -> Tuple: ...
    def config(self, param) -> Any: ...

class WLAN(AbstractNIC):
    def __init__(self, interface_id) -> None: ...
    def active(self, is_active: Optional[Any]) -> None: ...
    def connect(self, ssid: Any | None = ..., password: Any | None = ..., *, bssid: Any | None = ...) -> None: ...
    def disconnect(self) -> None: ...
    def scan(self) -> List[Tuple]: ...
    def status(self, param: Optional[Any]) -> Any: ...
    def isconnected(self) -> bool: ...
    def ifconfig(self, configtuple: Optional[Any]) -> Tuple: ...
    def config(self, param) -> Any: ...

class WLANWiPy(AbstractNIC):
    STA: Any
    AP: Any
    WEP: Any
    WPA: Any
    WPA2: Any
    INT_ANT: Any
    EXT_ANT: Any
    def __init__(self, id: int = ..., *args) -> None: ...
    def init(self, mode, ssid, auth, channel, antenna) -> Any: ...
    def connect(self, ssid, *, auth: Any | None = ..., bssid: Any | None = ..., timeout: Any | None = ...) -> None: ...
    def scan(self) -> List[Tuple]: ...
    def disconnect(self) -> None: ...
    def isconnected(self) -> bool: ...
    def ifconfig(self, if_id: int = ..., config: Union[str, Tuple] = ...) -> Tuple: ...
    def mode(self, mode: Optional[Any]) -> Any: ...
    def ssid(self, ssid: Optional[Any]) -> Any: ...
    def auth(self, auth: Optional[Any]) -> Any: ...
    def channel(self, channel: Optional[Any]) -> Any: ...
    def antenna(self, antenna: Optional[Any]) -> Any: ...
    def mac(self, mac_addr: Optional[Any]) -> bytes: ...
    def irq(self, handler, wake) -> Any: ...

class CC3K:
    WEP: Any
    WPA: Any
    WPA2: Any
    def __init__(self, spi, pin_cs, pin_en, pin_irq) -> None: ...
    def connect(self, ssid, key: Any | None = ..., *, security=..., bssid: Any | None = ...) -> None: ...
    def disconnect(self) -> None: ...
    def isconnected(self) -> bool: ...
    def ifconfig(self) -> Tuple: ...
    def patch_version(self) -> Any: ...
    def patch_program(self, cmd: str) -> Any: ...

class WIZNET5K:
    def __init__(self, spi, pin_cs, pin_rst) -> None: ...
    def isconnected(self) -> bool: ...
    def ifconfig(self, configtuple: Optional[Any]) -> Tuple: ...
    def regs(self) -> Any: ...
