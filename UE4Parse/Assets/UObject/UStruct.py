from typing import List, Tuple

from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Assets.UObject.FField import FField
from UE4Parse.Assets.UObject.UField import UField
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions.FCoreObjectVersion import FCoreObjectVersion
from UE4Parse.Versions.FFrameworkObjectVersion import FFrameworkObjectVersion


class UStruct(UField):
    SuperStruct: FPackageIndex
    Children: Tuple[FPackageIndex]
    ChildProperties: Tuple[FField]
    Script: bytes

    def __init__(self, reader: FAssetReader):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader
        self.SuperStruct = FPackageIndex(reader)

        if FFrameworkObjectVersion().get(reader) < FFrameworkObjectVersion.Type.RemoveUField_Next:
            firstChild = FPackageIndex(reader)
            self.Children = (firstChild,) if not firstChild.IsNull else ()
        else:
            self.Children = reader.readTArray(lambda : FPackageIndex(reader))

        if FCoreObjectVersion().get(reader) >= FCoreObjectVersion.Type.FProperties:
            self._deserialize_properties()

    def _deserialize_properties(self): # TODO: complete
        reader = self.reader
        # ChildProperties

        def read_property():
            raise NotImplementedError()
            pass


