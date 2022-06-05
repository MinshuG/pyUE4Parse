from enum import IntEnum, auto
from typing import List, Tuple, TYPE_CHECKING

from UE4Parse.IO.IoObjects.FFilePackageStoreEntry import FFilePackageStoreEntry
from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions import EUEVersion
from UE4Parse.Exceptions import ParserException

if TYPE_CHECKING:
    from UE4Parse.IoObjects.FImportedPackage import FPackageId

class EIoContainerHeaderVersion(IntEnum):
        BeforeVersionWasAdded = -1  # Custom constant to indicate pre-UE5 data
        Initial = 0
        LocalizedPackages = 1
        OptionalSegmentPackages = 2
        LatestPlusOne = auto()
        Latest = LatestPlusOne - 1

class FIoContainerHeader:
    Signature = 0x496f436e

    ContainerId: int  # FIoContainerId ulong
    # PackageCount: int
    ContainerNameMap: List['FNameEntrySerialized']
    PackageIds: List['FPackageId']
    StoreEntries: List[FFilePackageStoreEntry]

    def __init__(self, reader: FAssetReader, ueversion):
        if ueversion < EUEVersion.GAME_UE5_0:
            raise NotImplementedError()
        else:
            pass
        version = EIoContainerHeaderVersion.Initial

        if version == EIoContainerHeaderVersion.Initial:
            sign = reader.readUInt32()
            if sign != self.Signature:
                raise ParserException("Signature mismatch")
            version = EIoContainerHeaderVersion(reader.readInt32())

        self.ContainerId = reader.readUInt64()
        if version < EIoContainerHeaderVersion.OptionalSegmentPackages:
            PackageCount = reader.readUInt32()

        if version == EIoContainerHeaderVersion.BeforeVersionWasAdded:
            raise NotImplementedError()
        from UE4Parse.IoObjects.FImportedPackage import FPackageId
        self.PackageIds = list(reader.readTArray(FPackageId, reader))

        size = reader.readInt32()
        end = size + reader.tell()
        self.StoreEntries = list(reader.readTArray2(lambda: FFilePackageStoreEntry(reader, ueversion), len(self.PackageIds)))
        reader.seek(end, 0)

        if version >= EIoContainerHeaderVersion.Initial:
            self.ContainerNameMap = []
            FNameEntrySerialized.LoadNameBatch2(self.ContainerNameMap, reader)
