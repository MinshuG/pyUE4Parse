from enum import Enum

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.Structs.FSoftObjectPath import FSoftObjectPath


# from PropertyTagData.BaseProperty import ReadType


class SoftObjectProperty:
    position: int
    Value = None

    def __init__(self, reader: BinaryStream, readType: Enum) -> None:
        self.position = reader.base_stream.tell()
        self.Value = FSoftObjectPath(reader)
        if readType.value == 1:
            reader.seek(16 - (reader.base_stream.tell() - self.position))

    def GetValue(self):
        return self.Value.GetValue()
