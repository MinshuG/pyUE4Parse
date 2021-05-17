from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects import FName


class FSoftObjectPath:
    position: int
    AssetPathName: FName = FName
    SubPathString: str = None

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        self.AssetPathName = reader.readFName()
        self.SubPathString = reader.readString()

    def GetValue(self):
        return {
            "AssetPathName": self.AssetPathName.string,
            "SubPathString": self.SubPathString
        }
