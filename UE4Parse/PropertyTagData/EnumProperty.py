from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects import FPropertyTag
from UE4Parse.Objects.FName import FName


class EnumProperty:
    position: int
    Value: FName

    def __init__(self, reader: BinaryStream, tag: FPropertyTag, readType):
        self.position = reader.base_stream.tell()
        if readType.value != 69:  # luuuu
            self.Value = reader.readFName()
        else:
            byteValue = reader.readInt32() if tag.EnumName.string == "IntProperty" else reader.readByteToInt()
            self.Value = FName(reader.NameMap[byteValue], byteValue)

    def GetValue(self):
        return self.Value.GetValue()
