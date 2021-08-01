
from typing import TYPE_CHECKING
from UE4Parse.BinaryReader import BinaryStream

if TYPE_CHECKING:
    from UE4Parse.Assets.Objects.FPropertyTag import FPropertyTag

class BoolProperty:
    position: int
    Value: bool

    def __init__(self, reader: BinaryStream, tag: 'FPropertyTag', readType):  # for later use
        self.position = reader.base_stream.tell()
        if not reader.has_unversioned_properties and readType == 0:
            self.Value = getattr(tag, "BoolVal", True)
        elif readType.value in [0, 1, 2]:  # Normal, MAP and Array
            self.Value = bool(reader.readByteToInt())

    def GetValue(self):
        return self.Value
