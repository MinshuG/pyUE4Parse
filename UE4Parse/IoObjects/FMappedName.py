from typing import List
from enum import Enum
# from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized


class EType(Enum):
    Package = 0
    Container = 1
    Global = 2


class FMappedName:
    InvalidIndex = 0
    IndexBits = 30
    IndexMask = (1 << IndexBits) - 1
    TypeMask = ~IndexMask
    TypeShift = IndexBits

    Index: int
    Number: int
    _reader: object
    _globalNameMap: List[FNameEntrySerialized]

    def __init__(self) -> None:
        pass

    def isValid(self):
        return self.Index != self.InvalidIndex and self.Number != self.InvalidIndex

    def GetType(self):
        return int((self.Index & self.TypeMask) >> self.TypeShift)

    def IsGlobal(self):
        return ((self.Index & self.TypeMask) >> self.TypeShift) != 0
