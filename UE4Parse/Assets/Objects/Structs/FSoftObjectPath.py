from typing import TYPE_CHECKING, Optional
from UE4Parse.Assets.Objects.Common import StructInterface

from UE4Parse.Assets.Objects.FName import FName

if TYPE_CHECKING:
    from UE4Parse.Provider.Vfs.AbstractVfsFileProvider import AbstractVfsFileProvider
    from UE4Parse.Readers.FAssetReader import FAssetReader
    from UE4Parse.Assets.Exports.UObjects import UObject


class FSoftObjectPath(StructInterface):
    position: int
    AssetPathName: FName
    SubPathString: str

    def __init__(self, reader: Optional['FAssetReader'] = None) -> None:
        if reader:
            self.position = reader.base_stream.tell()
            self.AssetPathName = reader.readFName()
            self.SubPathString = reader.readFString()
        else:
            self.position = -1
            self.AssetPathName = FName("None")
            self.SubPathString = ""

    @classmethod
    def default(cls):
        return cls(None)

    def __str__(self):
        return self.AssetPathName.string

    def GetValue(self):
        return {
            "AssetPathName": self.AssetPathName.string,
            "SubPathString": self.SubPathString
        }

    def load(self, provider: 'AbstractVfsFileProvider') -> Optional['UObject']:
        if self.AssetPathName.string == "None":
            return None
        return provider.try_load_object(self.AssetPathName.string)
