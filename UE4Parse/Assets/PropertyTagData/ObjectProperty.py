from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex


class ObjectProperty:
    position: int
    Value: FPackageIndex

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        self.Value = FPackageIndex(reader)

    def GetValue(self):
        return self.Value.GetValue()
