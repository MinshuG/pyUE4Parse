from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects import FName


class FSmartName:
    position: int
    DisplayName: FName

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.DisplayName = reader.readFName()

    def GetValue(self):
        return {
            "DisplayName": self.DisplayName
        }
