from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects import FName


class DelegateProperty:
    position: int
    Object: int
    Name: FName

    def __init__(self, reader: BinaryStream) -> None:
        self.Object = reader.readInt32()
        self.Name = reader.readFName()

    def GetValue(self):
        return {
            "Object": self.Object,
            "Name": self.Name.string
        }
