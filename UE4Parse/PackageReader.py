from UE4Parse.IoObjects.FExportBundle import FExportBundle
from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry
from UE4Parse.IoObjects.FImportedPackage import FImportedPackage
from UE4Parse.IoObjects.FPackageSummary import FPackageSummary
from UE4Parse.Class.UStaticMesh import UStaticMesh
from typing import List, Any

from UE4Parse.Class.UStringTable import UStringTable
from UE4Parse.Class.UTexture2D import UTexture2D
from UE4Parse.Class.UObjects import UObject
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.IoObjects.IoUtils import resolveObjectIndex
from UE4Parse.Objects.FName import FName
from UE4Parse.Objects.FObjectExport import FObjectExport
from UE4Parse.Objects.FObjectImport import FObjectImport
from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Objects.FPackageFileSummary import FPackageFileSummary
from UE4Parse.Objects.FPackageIndex import FPackageIndex
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse import ToJson, Logger
from UE4Parse.Globals import Globals

logger = Logger.get_logger(__name__)


class LegacyPackageReader:
    NameMap: List[FNameEntrySerialized] = []
    ImportMap: List[FObjectImport] = []
    ExportMap: List[FObjectExport] = []
    DataExports: list = []
    DataExportTypes: List[FName] = []
    PackageFileSummary: FPackageFileSummary

    # @profile
    def __init__(self, uasset: BinaryStream, uexp: BinaryStream = None, ubulk: BinaryStream = None) -> None:
        self.reader = uasset

        self.reader.PackageReader = self
        self.PackageFileSummary = FPackageFileSummary(self.reader)
        pos = self.reader.tell()
        self.NameMap = self.SerializeNameMap()
        self.reader.NameMap = self.NameMap

        self.ImportMap = self.SerializeImportMap()
        self.ExportMap = self.SerializeExportMap()

        filever = self.PackageFileSummary.FileVersionUE4
        if filever > 0:
            self.reader.version = filever

        self.reader.ubulk_stream = ubulk

        if uexp is not None:
            self.reader.change_stream(uexp)
        elif self.PackageFileSummary.FileVersionUE4.value == 0:  # Cooked
            return
        else:  # not cooked
            self.reader.seek(pos, 0)
            self.reader.change_stream(self.reader.read())

        DataExports = []
        DataExportTypes: List[FName] = []
        for Export in self.ExportMap:
            if Export.ClassIndex.IsNull:
                ExportType = self.reader.readFName()
            elif Export.ClassIndex.IsExport:
                ExportType = self.ExportMap[Export.ClassIndex.AsExport].SuperIndex.Resource.ObjectName
            elif Export.ClassIndex.IsImport:
                ExportType = self.ImportMap[Export.ClassIndex.AsImport].ObjectName
            else:
                raise ParserException("failed to get export type")
            DataExportTypes.append(ExportType)

            ExportData: Any = None
            self.reader.seek(Export.SerialOffset - self.PackageFileSummary.TotalHeaderSize, 0)

            self.reader.bulk_offset = Export.SerialSize + self.PackageFileSummary.TotalHeaderSize  # ?

            pos = self.reader.base_stream.tell()
            if ExportType.string == "Texture2D":
                ExportData = UTexture2D(self.reader, ubulk, self.reader.bulk_offset)
            elif ExportType.string == "StaticMesh":
                ExportData = UStaticMesh(self.reader)
            elif ExportType.string == "StringTable":
                ExportData = UStringTable(self.reader)
            else:
                ExportData = UObject(self.reader)

            # export event
            trigger = Globals.Triggers.get(ExportType.string, False)
            if trigger:
                trigger(ExportData)

            position = self.reader.base_stream.tell()
            if self.reader.base_stream.tell() != pos + Export.SerialSize:
                logger.debug(
                    f"Didn't read ExportType {ExportType.string} properly, at {position}, should be: {pos + Export.SerialSize} behind: {pos + Export.SerialSize - position}")
            Export.exportObject = ExportData
            DataExports.append(ExportData)

        self.DataExports = DataExports
        self.DataExportTypes = DataExportTypes
        del self.reader

    def SerializeNameMap(self):
        if self.PackageFileSummary.NameCount > 0:
            self.reader.seek(self.PackageFileSummary.NameOffset, 0)
            OutNameMap: List[FNameEntrySerialized] = []
            for _ in range(self.PackageFileSummary.NameCount):
                OutNameMap.append(FNameEntrySerialized(self.reader))
            return OutNameMap
        return []

    def SerializeImportMap(self):
        if self.PackageFileSummary.ImportCount > 0:
            self.reader.seek(self.PackageFileSummary.ImportOffset, 0)
            OutImportMap: List[FObjectImport] = []
            for _ in range(self.PackageFileSummary.ImportCount):
                OutImportMap.append(FObjectImport(self.reader))
            return OutImportMap
        return []

    def SerializeExportMap(self):
        if self.PackageFileSummary.ExportCount > 0:
            self.reader.seek(self.PackageFileSummary.ExportOffset, 0)
            OutExportMap: List[FObjectExport] = []
            for _ in range(self.PackageFileSummary.ExportCount):
                OutExportMap.append(FObjectExport(self.reader))
            return OutExportMap
        return []

    def get_dict(self):
        return ToJson.ToJson(self)

    def find_export(self, export_name: str):
        for i in range(len(self.DataExportTypes)):
            export = self.DataExportTypes[i].string
            if export == export_name:
                return self.DataExports[i]
        return None

    def findObject(self, index: FPackageIndex):
        if index.IsNull:
            return None
        elif index.IsImport:
            return self.ImportMap[index.AsImport]
        else:  # index.IsExport
            export = self.ExportMap[index.AsExport]
            if hasattr(export, "exportObject"):
                return self.ExportMap[index.AsExport].exportObject
            return export


class IoPackageReader:
    GlobalData: FIoGlobalData
    Summary: FPackageSummary
    NameMap: List[FNameEntrySerialized]
    ImportMap: List[FPackageObjectIndex]
    ExportMap: List[FExportMapEntry]
    ExportBundle: FExportBundle
    GraphData: List[FImportedPackage]

    def __init__(self, uasset: BinaryStream, ubulk: BinaryStream, globalData: FIoGlobalData, provider,
                 onlyInfo: bool = False):
        reader = uasset
        reader.ubulk_stream = ubulk
        reader.PackageReader = self
        self.reader = reader

        self.Summary = FPackageSummary(reader=reader)

        self.NameMap = []

        nameHashes = []
        if self.Summary.NameMapNamesSize > 0:
            reader.seek(self.Summary.NameMapNamesOffset, 0)
            nameMapReader = BinaryStream(reader.readBytes(self.Summary.NameMapNamesSize))

            reader.seek(self.Summary.NameMapHashesOffset, 0)
            nameHashReader = BinaryStream(reader.readBytes(self.Summary.NameMapHashesSize))

            FNameEntrySerialized.LoadNameBatch(self.NameMap, nameHashes, nameMapReader, nameHashReader)
            del nameHashReader
            del nameMapReader

        self.ImportMap = []
        reader.seek(self.Summary.ImportMapOffset, 0)
        import_map_Count = int(
            (self.Summary.ExportMapOffset - self.Summary.ImportMapOffset) / 8)  # size of FPackageObjectIndex
        self.ImportMap = [FPackageObjectIndex(reader) for _ in range(import_map_Count)]

        self.ExportMap = []
        reader.seek(self.Summary.ExportMapOffset, 0)
        exportMapCount = int((self.Summary.ExportBundlesOffset - self.Summary.ExportMapOffset) / FExportMapEntry.SIZE)
        self.ExportMap = [FExportMapEntry(reader) for _ in range(exportMapCount)]

        self.ExportBundle = FExportBundle(reader)

        if not onlyInfo:
            reader.seek(self.Summary.GraphDataOffset, 0)
            GraphData = reader.readTArray(FImportedPackage, reader)


        breakpoint()

    def get_dict(self):
        return None
