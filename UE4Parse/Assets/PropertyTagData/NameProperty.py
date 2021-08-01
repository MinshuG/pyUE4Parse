from UE4Parse.BinaryReader import BinaryStream


class NameProperty:
    position: int
    Value: object  # FName

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readFName()

    def GetValue(self):
        return self.Value.GetValue()
