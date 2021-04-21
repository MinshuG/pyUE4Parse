from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Globals import Globals
from UE4Parse.Objects.EUEVersion import Versions
from UE4Parse.Objects.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version


class FStripDataFlags:
    globalStripFlags: int
    classStripFlags: int

    def __init__(self, reader: BinaryStream, min_version=Versions.VER_UE4_REMOVED_STRIP_DATA):
        if reader.version >= min_version:
            self.globalStripFlags = reader.readByteToInt()
            self.classStripFlags = reader.readByteToInt()
        else:
            self.globalStripFlags = 0
            self.classStripFlags = 0

    @property
    def isEditorDataStripped(self):
        return (self.globalStripFlags & 1) != 0

    @property
    def isDataStrippedForServer(self):
        return (self.globalStripFlags and 2) != 0

    def isClassDataStripped(self, flag: int):
        return (self.classStripFlags and flag) != 0

    def GetValue(self):
        return {
            "GlobalStripFlags": self.globalStripFlags,
            "ClassStripFlags": self.classStripFlags
        }
