from UE4Parse.BinaryReader import BinaryStream


class FloatProperty:
    position: int
    Value: float

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readFloat()

    def GetValue(self):
        return self.Value
