from enum import Enum
from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IoObjects.FMinimalName import FMinimalName
from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized


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
    _localNameMap: List[FNameEntrySerialized]

    def __init__(self, minimalName: FMinimalName = None, globalNameMap=None, localNameMap=None) -> None:
        if minimalName is None:
            return
        self.Index = minimalName.Index.Value
        self.Number = minimalName.Number
        self._globalNameMap = globalNameMap
        self._localNameMap = localNameMap

    def read(self, reader: BinaryStream):
        self.Index = reader.readUInt32()
        self.Number = reader.readUInt32()
        self._reader = reader
        return self

    def __str__(self):
        name_map = self._globalNameMap if self.IsGlobal() else self._reader.PackageReader.NameMap
        if name_map is None:
            return None
        index = self.GetIndex()
        if len(name_map) > index:
            return name_map[index].Name

    def GetValue(self):
        return self.__str__()

    def ToString(self):
        return self.__str__()

    def resolve(self, namemap):
        self._localNameMap = namemap
        return self.GetValue()

    def GetIndex(self):
        return self.Index & self.IndexMask

    def isValid(self):
        return self.Index != self.InvalidIndex and self.Number != self.InvalidIndex

    def GetType(self):
        return int((self.Index & self.TypeMask) >> self.TypeShift)

    def IsGlobal(self):
        return ((self.Index & self.TypeMask) >> self.TypeShift) != 0
