from enum import IntEnum
from typing import TYPE_CHECKING
from contextlib import suppress

from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.IoObjects.FMappedName import FMappedName
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.Assets.Objects.EObjectFlags import EObjectFlags

from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions import EUEVersion

if TYPE_CHECKING:
    from UE4Parse.Assets.Exports.UObjects import UObject


class EExportFilterFlags(IntEnum):
    Null = 0  # None
    NotForClient = 1
    NotForServer = 2


class FExportMapEntry:
    SIZE = 72
    CookedSerialOffset: int
    CookedSerialSize: int
    ObjectName: FMappedName
    OuterIndex: FPackageObjectIndex
    ClassIndex: FPackageObjectIndex
    SuperIndex: FPackageObjectIndex
    TemplateIndex: FPackageObjectIndex
    GlobalImportIndex: FPackageObjectIndex
    PublicExportHash: int
    ObjectFlags: EObjectFlags
    FilterFlags: EExportFilterFlags
    exportObject: 'UObject'
    type: FName = FName("Unknown")

    def __init__(self, reader: FAssetReader):
        self.CookedSerialOffset = reader.readUInt64()
        self.CookedSerialSize = reader.readUInt64()
        self.ObjectName = FMappedName().read(reader)
        self.OuterIndex = FPackageObjectIndex(reader)
        self.ClassIndex = FPackageObjectIndex(reader)
        self.SuperIndex = FPackageObjectIndex(reader)
        self.TemplateIndex = FPackageObjectIndex(reader)

        if reader.game >= EUEVersion.GAME_UE5_0:
            self.GlobalImportIndex = FPackageObjectIndex.from_int(0)
            self.PublicExportHash = reader.readUInt64()
        else:
            self.GlobalImportIndex = FPackageObjectIndex(reader)
            self.PublicExportHash = 0
        self.ObjectFlags = reader.readUInt32()
        with suppress(ValueError):
            self.ObjectFlags = EObjectFlags(self.ObjectFlags)
        self.FilterFlags = EExportFilterFlags(reader.readByteToInt())
        reader.seek(3)

    @property
    def name(self):
        return FName(self.ObjectName.GetValue())

