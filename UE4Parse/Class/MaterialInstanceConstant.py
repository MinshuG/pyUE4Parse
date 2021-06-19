from typing import Optional, List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Objects.FPackageIndex import FPackageIndex
from UE4Parse.PropertyTagData.StructProperty import StructProperty
from UE4Parse.provider import Provider


class UMaterialInstanceConstant(UObject):
    parent: Optional[FPackageIndex]
    ScalarParameterValues: Optional[List[StructProperty]]

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        self.parent = self.Dict.get("Parent", None)
        if self.parent is not None:
            self.parent = self.parent.Value

        self.ScalarParameterValues = self.Dict.get("ScalarParameterValues", None)
        self.VectorParameterValues = self.Dict.get("VectorParameterValues", None)
        self.TextureParameterValues = self.Dict.get("TextureParameterValues", None)

        for key, value in self.Dict.items():
            if hasattr(self, key):
                continue
            setattr(self, key, value)

    def get_parent(self):
        provider: Provider = self.reader.provider
        pkg = provider.get_package(self.parent)
        if pkg is not None:
            parent_mat = pkg.parse_package()
            return parent_mat
        return None
