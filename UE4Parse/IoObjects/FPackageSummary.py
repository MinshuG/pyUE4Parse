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
        self.PackageFlags = EPackageFlags(reader.readUInt32())
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


class FZenPackageSummary:
    bHasVersioningInfo: bool
    HeaderSize: int
    Name: FMappedName
    PackageFlags: int
    CookedHeaderSize: int
    ImportedPublicExportHashesOffset: int
    ImportMapOffset: int
    ExportMapOffset: int
    ExportBundleEntriesOffset: int
    GraphDataOffset: int

    def __init__(self, reader: BinaryStream):
        self.bHasVersioningInfo = reader.readBool()
        self.HeaderSize = reader.readUInt32()
        self.Name = FMappedName().read(reader)
        self.PackageFlags = EPackageFlags(reader.readUInt32())
        self.CookedHeaderSize = reader.readUInt32()
        self.ImportedPublicExportHashesOffset, self.ImportMapOffset, self.ExportMapOffset, self.ExportBundleEntriesOffset, self.GraphDataOffset = reader.unpack2('5i', 5*4)
