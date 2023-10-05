from typing import Tuple, Union, Dict, TYPE_CHECKING, Callable, Any

from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Assets.UObject.UField import UField
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions.FCoreObjectVersion import FCoreObjectVersion
from UE4Parse.Versions.FFrameworkObjectVersion import FFrameworkObjectVersion
from UE4Parse.Assets.UObject import FField


class UStruct(UField):
    SuperStruct: FPackageIndex
    Children: Union[Tuple[()], Tuple[FPackageIndex]]
    ChildProperties: Union[Tuple[()], Tuple['FField']]
    Script: bytes

    def __init__(self, reader: FAssetReader):
        super().__init__(reader)
        self.SuperStruct = FPackageIndex(0)
        self.Children = ()
        self.ChildProperties = ()

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader
        self.SuperStruct = FPackageIndex(reader)

        if FFrameworkObjectVersion().get(reader) < FFrameworkObjectVersion.Type.RemoveUField_Next:
            first_child = FPackageIndex(reader)
            self.Children = (first_child,) if not first_child.IsNull else ()
        else:
            self.Children = reader.readTArray(lambda: FPackageIndex(reader))

        if FCoreObjectVersion().get(reader) >= FCoreObjectVersion.Type.FProperties:
            self._deserialize_properties()

        bytecode_buffer_size = reader.readInt32()
        bytecode_size = reader.readInt32()
        reader.seek(bytecode_size, 1)

    def _deserialize_properties(self):
        reader = self.reader

        children = []
        num_prop = reader.readInt32()
        for i in range(num_prop):
            name = reader.readFName()
            prop = FField.construct(name)
            prop.deserialize(reader)
            children.append(prop)

        self.ChildProperties = tuple(children)

    def GetValue(self) -> Dict[str, Any]:
        props = super().GetValue()
        props["SuperStruct"] = self.SuperStruct.GetValue()
        props["Children"] = [child.GetValue() for child in self.Children]
        props["ChildProperties"] = [child.GetValue() for child in self.ChildProperties]
        return props
