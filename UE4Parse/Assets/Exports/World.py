from typing import Tuple

from UE4Parse.Assets.Objects.EUEVersion import EUEVersion
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Objects.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version


class UWorld(UObject):
    PersistentLevel: FPackageIndex  # UObject
    ExtraReferencedObjects: FPackageIndex
    StreamingLevels: Tuple[FPackageIndex]

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader
        if reader.game == EUEVersion.GAME_VALORANT: return  # prevent crash

        self.PersistentLevel = FPackageIndex(reader)  # reader.readObject()
        if reader.version < EUnrealEngineObjectUE4Version.VER_UE4_REMOVE_SAVEGAMESUMMARY:
            dummy_object = FPackageIndex(reader)
        self.ExtraReferencedObjects = FPackageIndex(reader)
        self.StreamingLevels = reader.readTArray(FPackageIndex, reader)

    def GetValue(self) -> dict:
        props = super().GetValue()
        props["PersistentLevel"] = self.PersistentLevel.GetValue()
        props["ExtraReferencedObjects"] = self.ExtraReferencedObjects.GetValue()
        props["StreamingLevels"] = [x.GetValue() for x in self.StreamingLevels]
        return props
