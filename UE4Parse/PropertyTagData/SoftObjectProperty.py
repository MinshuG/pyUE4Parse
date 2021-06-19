from enum import Enum
from typing import TYPE_CHECKING

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.Structs.FSoftObjectPath import FSoftObjectPath

if TYPE_CHECKING:
    from .BaseProperty import ReadType


class SoftObjectProperty:
    position: int
    Value = None

    def __init__(self, reader: BinaryStream, readType: 'ReadType') -> None:
        self.position = reader.base_stream.tell()
        self.Value = FSoftObjectPath(reader)

        from .BaseProperty import ReadType
        if reader.has_unversioned_properties:
            return
        if readType == ReadType.MAP:
            reader.seek(16 - (reader.base_stream.tell() - self.position))

    def GetValue(self):
        return self.Value.GetValue()
