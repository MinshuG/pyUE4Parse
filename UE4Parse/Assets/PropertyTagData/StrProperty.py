from UE4Parse.BinaryReader import BinaryStream


class StrProperty:
    Value: str
    position: int

    def __init__(self, reader: BinaryStream, readType) -> None:
        self.position = reader.base_stream.tell()
        if readType.value == 3:
            self.Value = ""
        else:
            self.Value = reader.readFString()

    def GetValue(self):
        return self.Value