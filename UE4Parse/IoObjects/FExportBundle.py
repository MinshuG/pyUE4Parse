from enum import IntEnum
from typing import List, Tuple

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions.EUEVersion import EUEVersion


class EExportCommandType(IntEnum):
    ExportCommandType_Create = 0
    ExportCommandType_Serialize = 1
    ExportCommandType_Count = 2


class FExportBundleHeader:
    SerialOffset: int
    FirstEntryIndex: int
    EntryCount: int

    def __init__(self, reader: FAssetReader):
        self.SerialOffset = reader.readUInt64() if reader.version <= EUEVersion.GAME_UE5_0 else -1
        self.FirstEntryIndex = reader.readUInt32()
        self.EntryCount = reader.readUInt32()


class FExportBundleEntry:
    LocalExportIndex: int
    CommandType: EExportCommandType

    def __init__(self, reader: BinaryStream):
        self.LocalExportIndex = reader.readUInt32()
        self.CommandType = EExportCommandType(reader.readUInt32())


class FExportBundle:
    Headers: List[FExportBundleHeader]
    Entries: Tuple[FExportBundleEntry]

    def __init__(self, reader: BinaryStream):
        self.Headers = list((FExportBundleHeader(reader),))
        self.Entries = tuple(FExportBundleEntry(reader) for _ in range(self.Headers[0].EntryCount))

    @classmethod
    def from_data(cls, headers, entries):
        inst = cls.__new__(cls)
        inst.Headers = headers
        inst.Entries = entries
        return inst
