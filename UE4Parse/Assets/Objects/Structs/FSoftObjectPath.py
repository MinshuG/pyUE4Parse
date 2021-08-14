from typing import Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName


class FSoftObjectPath:
    position: int
    AssetPathName: FName = FName
    SubPathString: str = None

    def __init__(self, reader: Optional[BinaryStream] = None) -> None:
        if reader:
            self.position = reader.base_stream.tell()
            self.AssetPathName = reader.readFName()
            self.SubPathString = reader.readFString()
        else:
            self.position = -1
            self.AssetPathName = FName("None")  # Zero read?
            self.SubPathString = ""

    def __str__(self):
        return self.AssetPathName.string

    def GetValue(self):
        return {
            "AssetPathName": self.AssetPathName.string,
            "SubPathString": self.SubPathString
        }
