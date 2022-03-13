from UE4Parse.BinaryReader import BinaryStream


class DoubleProperty:
    position: int
    Value: float

    def __init__(self, reader: BinaryStream, readType):
        self.position = reader.base_stream.tell()
        if readType.value == 3:  # zero
            self.Value = 0.0
        else:
            self.Value = reader.readDouble()

    def GetValue(self):
        return self.Value
