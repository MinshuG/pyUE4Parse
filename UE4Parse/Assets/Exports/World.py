from typing import Tuple

from UE4Parse.Versions.EUEVersion import EUEVersion
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Versions.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version
from UE4Parse.Assets.Exports.ExportRegistry import register_export


@register_export
class UWorld(UObject):
    PersistentLevel: FPackageIndex  # UObject
    ExtraReferencedObjects: FPackageIndex
    StreamingLevels: Tuple[FPackageIndex]

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader

        self.PersistentLevel = FPackageIndex(reader)
        self.ExtraReferencedObjects = FPackageIndex(reader)
        self.StreamingLevels = reader.readTArray(FPackageIndex, reader)

    def GetValue(self) -> dict:
        props = super().GetValue()
        props["PersistentLevel"] = self.PersistentLevel.GetValue()
        props["ExtraReferencedObjects"] = self.ExtraReferencedObjects.GetValue()
        props["StreamingLevels"] = [x.GetValue() for x in self.StreamingLevels]
        return props
