from typing import Any, Optional

class sha256:
    def __init__(self, data: Optional[Any]) -> None: ...

class hash:
    def update(self, data) -> Any: ...
    def digest(self) -> bytes: ...
    def hexdigest(self) -> Any: ...

class sha1(hash):
    def __init__(self, data: Optional[Any]) -> None: ...

class md5(hash):
    def __init__(self, data: Optional[Any]) -> None: ...
