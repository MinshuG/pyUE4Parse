from UE4Parse.Objects.EUEVersion import EUEVersion
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Objects.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version


class UWorld(UObject):
    PersistentLevel: UObject
    ExtraReferencedObjects: UObject
    StreamingLevels: UObject

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader
        if reader.game == EUEVersion.GAME_VALORANT: return # prevent crash

        self.PersistentLevel = reader.readObject()
        if reader.version < EUnrealEngineObjectUE4Version.VER_UE4_REMOVE_SAVEGAMESUMMARY:
            dummy_object = reader.readObject()
        self.ExtraReferencedObjects = reader.readObject()
        self.StreamingLevels = reader.readObject()
