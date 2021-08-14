from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from UE4Parse.PakFile.PakReader import PakReader
    from UE4Parse.IO.IoStoreReader import FFileIoStoreReader


class GameFile(ABC):
    Name: str
    Encrypted: bool
    CompressionMethodIndex: int
    Container: Union['FFileIoStoreReader', 'PakReader']

    def __init__(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    def __repr__(self):
        return f"<Name={self.Name}>"
