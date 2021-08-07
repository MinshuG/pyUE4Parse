from UE4Parse.Assets.Objects.EPackageFlags import EPackageFlags
from .FMappedName import FMappedName
from ..BinaryReader import BinaryStream
from contextlib import suppress


class FPackageSummary:
    Name: FMappedName
    SourceName: FMappedName
    PackageFlags: int
    CookedHeaderSize: int
    NameMapNamesOffset: int
    NameMapNamesSize: int
    NameMapHashesOffset: int
    NameMapHashesSize: int
    ImportMapOffset: int
    ExportMapOffset: int
    ExportBundlesOffset: int
    GraphDataOffset: int
    GraphDataSize: int

    def __init__(self, reader: BinaryStream) -> None:
        self.Name = FMappedName().read(reader)
        self.SourceName = FMappedName().read(reader)
        self.PackageFlags = reader.readUInt32()
        with suppress(ValueError):
            self.PackageFlags = EPackageFlags(self.PackageFlags)
        self.CookedHeaderSize = reader.readUInt32()
        self.NameMapNamesOffset = reader.readInt32()
        self.NameMapNamesSize = reader.readInt32()
        self.NameMapHashesOffset = reader.readInt32()
        self.NameMapHashesSize = reader.readInt32()
        self.ImportMapOffset = reader.readInt32()
        self.ExportMapOffset = reader.readInt32()
        self.ExportBundlesOffset = reader.readInt32()
        self.GraphDataOffset = reader.readInt32()
        self.GraphDataSize = reader.readInt32()
