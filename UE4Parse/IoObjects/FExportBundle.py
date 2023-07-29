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
        self.SerialOffset = reader.readUInt64() if reader.game >= EUEVersion.GAME_UE5_0 else -1
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

    def __init__(self, reader: BinaryStream, graphdatasize: int):
        remainingBundleEntryCount = graphdatasize // (4+4)
        """
        var foundBundlesCount = 0;
        var foundBundleHeaders = new List<FExportBundleHeader>();
        while (foundBundlesCount < remainingBundleEntryCount)
        {
            // This location is occupied by header, so it is not a bundle entry
            remainingBundleEntryCount--;
            var bundleHeader = new FExportBundleHeader(Ar);
            foundBundlesCount += (int) bundleHeader.EntryCount;
            foundBundleHeaders.Add(bundleHeader);
        }
        """
        foundBundlesCount = 0
        foundBundleHeaders = []
        while foundBundlesCount < remainingBundleEntryCount:
            remainingBundleEntryCount -= 1
            bundleHeader = FExportBundleHeader(reader)
            foundBundlesCount += bundleHeader.EntryCount
            foundBundleHeaders.append(bundleHeader)

        self.Headers = foundBundleHeaders
        self.Entries = reader.readTArray2(FExportBundleEntry, foundBundlesCount, reader)

    @classmethod
    def from_data(cls, headers, entries):
        inst = cls.__new__(cls)
        inst.Headers = headers
        inst.Entries = entries
        return inst
