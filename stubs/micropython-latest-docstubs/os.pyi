from typing import Any, IO, Iterator, Optional, Tuple

class VfsFat:
    def __init__(self, block_dev) -> None: ...
    @staticmethod
    def mkfs(block_dev) -> None: ...

class VfsLfs1:
    def __init__(self, block_dev, readsize: int = ..., progsize: int = ..., lookahead: int = ...) -> None: ...
    @staticmethod
    def mkfs(block_dev, readsize: int = ..., progsize: int = ..., lookahead: int = ...) -> None: ...

class VfsLfs2:
    def __init__(self, block_dev, readsize: int = ..., progsize: int = ..., lookahead: int = ..., mtime: bool = ...) -> None: ...
    @staticmethod
    def mkfs(block_dev, readsize: int = ..., progsize: int = ..., lookahead: int = ...) -> None: ...

class AbstractBlockDev:
    def __init__(self, *args) -> None: ...
    def readblocks(self, block_num, buf, offset: Optional[int]) -> Any: ...
    def writeblocks(self, block_num, buf, offset: Optional[int]) -> Any: ...
    def ioctl(self, op, arg) -> int: ...

def uname() -> Tuple: ...
def urandom(n) -> bytes: ...
def chdir(path) -> Any: ...
def getcwd() -> Any: ...
def ilistdir(dir: Optional[Any]) -> Iterator[Tuple]: ...
def listdir(dir: Optional[Any]) -> Any: ...
def mkdir(path) -> Any: ...
def remove(path) -> None: ...
def rmdir(path) -> None: ...
def rename(old_path, new_path) -> None: ...
def stat(path) -> Any: ...
def statvfs(path) -> Tuple: ...
def sync() -> None: ...
def dupterm(stream_object, index: int = ...) -> IO: ...
def mount(fsobj, mount_point, readonly) -> Any: ...
def umount(mount_point) -> Any: ...
