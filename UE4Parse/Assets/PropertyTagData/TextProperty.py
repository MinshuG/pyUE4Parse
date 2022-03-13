from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FText import FText


class TextProperty:
    position: int
    Value = None

    def __init__(self, reader: BinaryStream, readType) -> None:
        self.position = reader.base_stream.tell()
        if readType.value == 3:
            self.Value = FText.default()
        else:
            self.Value = FText(reader)

    def GetValue(self):
        return self.Value.GetValue()
