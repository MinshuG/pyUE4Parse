from enum import IntEnum

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IoObjects.FMappedName import FMappedName
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.Objects.EObjectFlags import EObjectFlags


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
    ObjectFlags: EObjectFlags
    FilterFlags: EExportFilterFlags

    def __init__(self, reader: BinaryStream):
        self.CookedSerialOffset = reader.readUInt64()
        self.CookedSerialSize = reader.readUInt64()
        self.ObjectName = FMappedName().read(reader)
        self.OuterIndex = FPackageObjectIndex(reader)
        self.ClassIndex = FPackageObjectIndex(reader)
        self.SuperIndex = FPackageObjectIndex(reader)
        self.TemplateIndex = FPackageObjectIndex(reader)
        self.GlobalImportIndex = FPackageObjectIndex(reader)
        self.ObjectFlags = reader.readUInt32()
        try:
            self.ObjectFlags = EObjectFlags(self.ObjectFlags)
        except:
            pass

        self.FilterFlags = EExportFilterFlags(reader.readByteToInt())
        reader.seek(3)

    def GetValue(self):
        return {
            "ClassIndex": "TODO",  # self.ClassIndex.GetValue(),
            "SuperIndex": "TODO",  # self.SuperIndex.GetValue(),
            "OuterIndex": "TODO",  # self.OuterIndex.GetValue(),
            "ObjectName": self.ObjectName.GetValue()
        }
