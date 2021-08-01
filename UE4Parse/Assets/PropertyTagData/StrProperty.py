from UE4Parse.BinaryReader import BinaryStream


class StrProperty:
    Value: str
    position: int

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        self.Value = reader.readFString()

    def GetValue(self):
        return self.Value