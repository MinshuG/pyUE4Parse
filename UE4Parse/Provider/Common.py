from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from UE4Parse.BinaryReader import BinaryStream
    from UE4Parse.PakFile.PakReader import PakReader
    from UE4Parse.IO.IoStoreReader import FFileIoStoreReader


class GameFile(ABC):
    __slots__ = ("Name", "Encrypted", "CompressionMethodIndex", "Container", "ubulk", "uexp", "uptnl")
    Name: str
    Encrypted: bool
    CompressionMethodIndex: int
    Container: Union['FFileIoStoreReader', 'PakReader']
    ubulk: 'GameFile'
    uexp: 'GameFile'
    uptnl: 'GameFile'

    def __init__(self):
        pass

    @abstractmethod
    def get_size(self) -> int:
        ...

    @abstractmethod
    def get_data(self) -> 'BinaryStream':
        ...

    def __repr__(self):
        return f"<Name={self.Name}>"
