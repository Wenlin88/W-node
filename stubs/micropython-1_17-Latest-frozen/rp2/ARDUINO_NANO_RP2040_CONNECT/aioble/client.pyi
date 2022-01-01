from .core import GattError as GattError, ble as ble, register_irq_handler as register_irq_handler
from .device import DeviceConnection as DeviceConnection
from typing import Any

_IRQ_GATTC_SERVICE_RESULT: Any
_IRQ_GATTC_SERVICE_DONE: Any
_IRQ_GATTC_CHARACTERISTIC_RESULT: Any
_IRQ_GATTC_CHARACTERISTIC_DONE: Any
_IRQ_GATTC_DESCRIPTOR_RESULT: Any
_IRQ_GATTC_DESCRIPTOR_DONE: Any
_IRQ_GATTC_READ_RESULT: Any
_IRQ_GATTC_READ_DONE: Any
_IRQ_GATTC_WRITE_DONE: Any
_IRQ_GATTC_NOTIFY: Any
_IRQ_GATTC_INDICATE: Any
_CCCD_UUID: Any
_CCCD_NOTIFY: Any
_CCCD_INDICATE: Any
_FLAG_READ: Any
_FLAG_WRITE_NO_RESPONSE: Any
_FLAG_WRITE: Any
_FLAG_NOTIFY: Any
_FLAG_INDICATE: Any

def _client_irq(event, data) -> None: ...

class ClientDiscover:
    _connection: Any
    _queue: Any
    _status: Any
    _event: Any
    _disc_type: Any
    _parent: Any
    _timeout_ms: Any
    _args: Any
    def __init__(self, connection, disc_type, parent, timeout_ms, *args) -> None: ...
    async def _start(self) -> None: ...
    def __aiter__(self): ...
    async def __anext__(self): ...
    def _discover_result(conn_handle, *args) -> None: ...
    def _discover_done(conn_handle, status) -> None: ...

class ClientService:
    connection: Any
    _start_handle: Any
    _end_handle: Any
    uuid: Any
    def __init__(self, connection, start_handle, end_handle, uuid) -> None: ...
    def __str__(self): ...
    async def characteristic(self, uuid, timeout_ms: int = ...): ...
    def characteristics(self, uuid: Any | None = ..., timeout_ms: int = ...): ...
    def _start_discovery(connection, uuid: Any | None = ...) -> None: ...

class BaseClientCharacteristic:
    def _register_with_connection(self) -> None: ...
    def _find(conn_handle, value_handle): ...
    def _check(self, flag) -> None: ...
    _read_status: Any
    _read_event: Any
    async def read(self, timeout_ms: int = ...): ...
    def _read_result(conn_handle, value_handle, data) -> None: ...
    def _read_done(conn_handle, value_handle, status) -> None: ...
    _write_status: Any
    _write_event: Any
    async def write(self, data, response: bool = ..., timeout_ms: int = ...) -> None: ...
    def _write_done(conn_handle, value_handle, status) -> None: ...

class ClientCharacteristic(BaseClientCharacteristic):
    service: Any
    connection: Any
    _def_handle: Any
    _value_handle: Any
    properties: Any
    uuid: Any
    _read_event: Any
    _read_data: Any
    _read_status: Any
    _write_event: Any
    _write_status: Any
    _notify_event: Any
    _notify_queue: Any
    _indicate_event: Any
    _indicate_queue: Any
    def __init__(self, service, def_handle, value_handle, properties, uuid) -> None: ...
    def __str__(self): ...
    def _connection(self): ...
    async def descriptor(self, uuid, timeout_ms: int = ...): ...
    def descriptors(self, timeout_ms: int = ...): ...
    def _start_discovery(service, uuid: Any | None = ...) -> None: ...
    async def _notified_indicated(self, queue, event, timeout_ms): ...
    async def notified(self, timeout_ms: Any | None = ...): ...
    def _on_notify_indicate(self, queue, event, data) -> None: ...
    def _on_notify(conn_handle, value_handle, notify_data) -> None: ...
    async def indicated(self, timeout_ms: Any | None = ...): ...
    def _on_indicate(conn_handle, value_handle, indicate_data) -> None: ...
    async def subscribe(self, notify: bool = ..., indicate: bool = ...) -> None: ...

class ClientDescriptor(BaseClientCharacteristic):
    characteristic: Any
    uuid: Any
    _value_handle: Any
    properties: Any
    def __init__(self, characteristic, dsc_handle, uuid) -> None: ...
    def __str__(self): ...
    def _connection(self): ...
    def _start_discovery(characteristic, uuid: Any | None = ...) -> None: ...