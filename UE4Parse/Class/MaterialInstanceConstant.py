from typing import Optional, List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Objects.FPackageIndex import FPackageIndex
from UE4Parse.PropertyTagData.StructProperty import StructProperty
from UE4Parse.provider import Provider


class UMaterialInstanceConstant(UObject):
    parent: Optional[FPackageIndex]
    ScalarParameterValues: Optional[List[StructProperty]]

    def __init__(self, reader: BinaryStream, validpos):
        super().__init__(reader, validpos=validpos)
        self.parent = self.Dict.get("Parent", None)
        if self.parent is not None:
            self.parent = self.parent.Value

        self.ScalarParameterValues = self.Dict.get("ScalarParameterValues", None)
        self.VectorParameterValues = self.Dict.get("VectorParameterValues", None)
        self.TextureParameterValues = self.Dict.get("TextureParameterValues", None)

    # def merge_with_parent(self):
    #     provider: Provider = self.reader.provider
    #     pkg = provider.get_package(self.parent)
    #     parent_mat = pkg.parse_package()
    #     materialexport = parent_mat.find_export("Material")
    #     if materialexport is not None:
    #         materialexport = materialexport.exportObject
    #     else:
    #         return
    #     self.Dict = materialexport.Dict.update(self.Dict)
