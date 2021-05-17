from typing import List, Dict

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO.IoObjects.FIoStoreTocHeader import FIoContainerId
from UE4Parse.IoObjects.FImportedPackage import FPackageId

FSourceToLocalizedPackageIdMap = List[Dict[FPackageId, FPackageId]]  # pair ??
FCulturePackageMap = Dict[str, FSourceToLocalizedPackageIdMap]


class FContainerHeader:
    ContainerId: FIoContainerId
    PackageCount: int
    Names: List[int]
    NameHashes: List[int]
    PackageIds: List[FPackageId]
    StoreEntries: List[int]
    CulturePackageMap: FCulturePackageMap
    PackageRedirects: List[Dict[FPackageId, FPackageId]]

    def __init__(self, reader: BinaryStream):
        self.ContainerId = FIoContainerId(reader)
        self.PackageCount = reader.readUInt32()
        self.Names = reader.readBytes(reader.readInt32())
        self.NameHashes = reader.readBytes(reader.readInt32())
        self.PackageIds = reader.readTArray(FPackageId, reader)
        self.StoreEntries = reader.readTArray(reader.readByteToInt)
        # self.CulturePackageMap = FCulturePackageMap
