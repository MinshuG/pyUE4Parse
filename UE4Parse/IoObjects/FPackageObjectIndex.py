from enum import IntEnum, auto
from typing import Optional

from UE4Parse.BinaryReader import BinaryStream


class EType(IntEnum):
    Export = 0
    ScriptImport = auto()
    PackageImport = auto()
    Null = auto()
    TypeCount = Null


class FPackageObjectIndex:
    IndexBits = 62
    IndexMask = (1 << IndexBits) - 1
    TypeMask = ~IndexMask
    TypeShift = IndexBits
    Invalid = ~0

    _typeAndId: int

    @property
    def Type(self):
        return EType(self._typeAndId >> self.TypeShift)

    @property
    def Value(self):
        return self._typeAndId & self.IndexMask

    @property
    def IsNull(self):
        return self._typeAndId == self.Invalid

    @property
    def IsExport(self):
        return self.Type == EType.Export

    @property
    def IsScriptImport(self):
        return self.Type == EType.ScriptImport

    @property
    def IsPackageImport(self):
        return self.Type == EType.PackageImport

    @property
    def AsExport(self):  # ToExport
        assert self.IsExport
        return self._typeAndId

    def __init__(self, reader: Optional[BinaryStream] = None, type_and_id: Optional[int] = None):
        if reader is None:
            self._typeAndId = type_and_id
        else:
            self._typeAndId = reader.readUInt64()

    def __eq__(self, o: 'FPackageObjectIndex') -> bool:
        return self.typeAndId == o.typeAndId

    @property
    def typeAndId(self):
        return self._typeAndId

    def GetValue(self):
        return {
            "typeAndId" : self.typeAndId,
            "Type": self.Type,
            "Value": self.Value
        }
