from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex


class ObjectProperty:
    position: int
    Value: FPackageIndex

    def __init__(self, reader: BinaryStream, readType) -> None:
        self.position = reader.base_stream.tell()
        if readType.value == 3:
            self.Value = FPackageIndex(0)
        else:
            self.Value = FPackageIndex(reader)

    def GetValue(self):
        return self.Value.GetValue()
