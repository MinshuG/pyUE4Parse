from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.BinaryReader import BinaryStream


class NameProperty:
    position: int
    Value: object  # FName

    def __init__(self, reader: BinaryStream, readType):
        self.position = reader.base_stream.tell()
        if readType.value == 3:
            self.Value = FName("None")
        else:
            self.Value = reader.readFName()

    def GetValue(self):
        return self.Value.GetValue()
