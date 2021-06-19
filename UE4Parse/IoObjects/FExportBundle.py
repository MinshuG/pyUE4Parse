from enum import IntEnum
from typing import List, Tuple

from UE4Parse.BinaryReader import BinaryStream


class EExportCommandType(IntEnum):
    ExportCommandType_Create = 0
    ExportCommandType_Serialize = 1
    ExportCommandType_Count = 2


class FExportBundleHeader:
    FirstEntryIndex: int
    EntryCount: int

    def __init__(self, reader: BinaryStream):
        self.FirstEntryIndex = reader.readUInt32()
        self.EntryCount = reader.readUInt32()


class FExportBundleEntry:
    LocalExportIndex: int
    CommandType: EExportCommandType

    def __init__(self, reader: BinaryStream):
        self.LocalExportIndex = reader.readUInt32()
        self.CommandType = EExportCommandType(reader.readUInt32())


class FExportBundle:
    Header: FExportBundleHeader
    Entries: Tuple[FExportBundleEntry]

    def __init__(self, reader: BinaryStream):
        self.Header = FExportBundleHeader(reader) # multiple header?
        self.Entries = tuple(FExportBundleEntry(reader) for _ in range(self.Header.EntryCount))

    def getOrder(self):
        y = []
        for x in self.Entries:
            if x.CommandType == EExportCommandType.ExportCommandType_Serialize:
                y.append(min(self.Header.EntryCount - 1, x.LocalExportIndex))
        return y
