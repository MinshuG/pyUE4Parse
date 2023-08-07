from typing import TYPE_CHECKING, Mapping, Dict, Tuple, Union

from ..Objects.FPackageIndex import FPackageIndex
from ..UObject import UStruct
from ...Versions.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version
from ..Objects.FName import FName

if TYPE_CHECKING:
    from ...Readers.FAssetReader import FAssetReader


class UClass(UStruct):
    FuncMap: Dict['FName', 'FPackageIndex']
    ClassFlags: int
    ClassWithin: 'FPackageIndex'
    ClassConfigName: 'FName'
    ClassGeneratedBy: 'FPackageIndex'
    Interfaces: Union[Tuple[()], Tuple['FImplementedInterface']]
    bCooked: bool
    ClassDefaultObject: 'FPackageIndex'

    def __init__(self, reader: 'FAssetReader'):
        super().__init__(reader)
        self.bCooked = False
        self.ClassDefaultObject = FPackageIndex(0)
        self.Interfaces = ()
        self.ClassGeneratedBy = FPackageIndex(0)
        self.ClassConfigName = FName("None", -1)
        self.ClassWithin = FPackageIndex(0)
        self.ClassFlags = 0
        self.FuncMap = {}

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader
        from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex

        for i in range(reader.readInt32()):  # numfunc
            self.FuncMap[reader.readFName()] = FPackageIndex(reader)

        self.ClassFlags = reader.readUInt32()

        self.ClassWithin = FPackageIndex(reader)
        self.ClassConfigName = reader.readFName()
        self.ClassGeneratedBy = FPackageIndex(reader)

        self.Interfaces = reader.readTArray(FImplementedInterface, reader)

        bdeprecated_read_order = reader.readBool()
        dummy = reader.readFName()

        if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_ADD_COOKED_TO_UCLASS:
            self.bCooked = reader.readBool()

        self.ClassDefaultObject = FPackageIndex(reader)

    def GetValue(self):
        props = super().GetValue()
        props["ClassFlags"] = self.ClassFlags
        props["ClassWithin"] = self.ClassWithin.GetValue()
        props["ClassConfigName"] = self.ClassConfigName.string
        props["ClassGeneratedBy"] = self.ClassGeneratedBy.GetValue()
        props["Interfaces"] = [i.Class.GetValue() for i in self.Interfaces]
        props["bCooked"] = self.bCooked
        props["ClassDefaultObject"] = self.ClassDefaultObject.GetValue()
        return props


class FImplementedInterface:
    def __init__(self, reader: 'FAssetReader'):
        self.Class = FPackageIndex(reader)
        self.PointerOffset = reader.readInt32()
        self.bImplementedByK2 = reader.readBool()
