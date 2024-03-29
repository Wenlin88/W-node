from typing import Any, Optional

MONO_VLSB: bytes
MONO_HLSB: bytes
MONO_HMSB: bytes
RGB565: Any
GS2_HMSB: Any
GS4_HMSB: Any
GS8: Any

class FrameBuffer:
    def __init__(self, buffer, width, height, format, stride: int = ...) -> None: ...
    def fill(self, c) -> None: ...
    def pixel(self, x, y, c: Optional[Any]) -> Any: ...
    def hline(self, x, y, w, c) -> Any: ...
    def vline(self, x, y, h, c) -> Any: ...
    def line(self, x1, y1, x2, y2, c) -> None: ...
    def rect(self, x, y, w, h, c) -> Any: ...
    def fill_rect(self, x, y, w, h, c) -> None: ...
    def text(self, s, x, y, c: Optional[Any]) -> None: ...
    def scroll(self, xstep, ystep) -> Any: ...
    def blit(self, fbuf, x, y, key: int = ..., palette: Any | None = ...) -> None: ...
