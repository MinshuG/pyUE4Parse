from UE4Parse.BinaryReader import BinaryStream


class BoolProperty:
    position: int
    Value: bool

    def __init__(self, reader: BinaryStream, tag, readType):  # for later use
        self.position = reader.base_stream.tell()
        if readType.value in [0, 1]:  # Normal and MAP
            self.Value = bool(tag.BoolVal)
        elif readType.value == 2:  # Array
            self.Value = bool(reader.readByteToInt())

    def GetValue(self):
        return self.Value
