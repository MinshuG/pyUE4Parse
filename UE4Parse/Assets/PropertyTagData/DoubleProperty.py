from UE4Parse.BinaryReader import BinaryStream


class DoubleProperty:
    def __init__(self, reader: BinaryStream):
        self.Value = reader.readDouble()

    def GetValue(self):
        return self.Value
