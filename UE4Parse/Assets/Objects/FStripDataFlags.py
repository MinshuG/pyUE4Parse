from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import Versions


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

    def isEditorDataStripped(self):
        return (self.globalStripFlags & 1) != 0

    def isDataStrippedForServer(self):
        return (self.globalStripFlags & 2) != 0

    def isClassDataStripped(self, flag: int):
        return (self.classStripFlags & flag) != 0

    def GetValue(self):
        return {
            "GlobalStripFlags": self.globalStripFlags,
            "ClassStripFlags": self.classStripFlags
        }
