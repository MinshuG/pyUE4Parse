from UE4Parse.IoObjects.IoUtils import resolveObjectIndex
from typing import List, TYPE_CHECKING, Optional, Tuple, Union

from UE4Parse import Logger
from UE4Parse.Assets import ToJson
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.IoObjects.FExportBundle import EExportCommandType, FExportBundle
from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry
from UE4Parse.IoObjects.FImportedPackage import FImportedPackage
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.IoObjects.FPackageSummary import FPackageSummary
from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Assets.Objects.FObjectExport import FObjectExport
from UE4Parse.Assets.Objects.FObjectImport import FObjectImport
from UE4Parse.Assets.Objects.FPackageFileSummary import FPackageFileSummary
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Assets.Exports.ExportRegistry import Registry

if TYPE_CHECKING:
    from UE4Parse.Provider import Provider

logger = Logger.get_logger(__name__)


class Package:
    NameMap: List[FNameEntrySerialized] = []
    ImportMap: Tuple[Union[FObjectImport, FPackageObjectIndex]] = []
    ExportMap: Tuple[FObjectExport, FExportMapEntry] = []
    Summary: Union[FPackageFileSummary, FPackageSummary]
    Provider: 'Provider'

    def get_summary(self) -> FPackageFileSummary:
        return self.Summary

    def get_dict(self):
        return ToJson.ToJson(self)

    def find_export(self, export_name: str) -> Optional[Union[FObjectExport, FExportMapEntry]]:
        for export in self.ExportMap:
            if export_name == export.name.string:
                return export
        return None


class LegacyPackageReader(Package):
    NameMap: List[FNameEntrySerialized] = []
    ImportMap: List[FObjectImport] = []
    ExportMap: List[FObjectExport] = []
    Summary: FPackageFileSummary

    # @profile
    def __init__(self, uasset: BinaryStream, uexp: BinaryStream = None, ubulk: BinaryStream = None,
                 provider: "Provider" = None) -> None:
        self.reader = uasset
        self.reader.set_ar_version(provider.GameInfo.UEVersion)
        self.reader.provider = provider
        self.reader.PackageReader = self

        self.PackageFileSummary = FPackageFileSummary(self.reader)
        self.Summary = self.PackageFileSummary
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

        for Export in self.ExportMap:
            if Export.ClassIndex.IsNull:
                ExportType = self.reader.readFName()
            elif Export.ClassIndex.IsExport:
                ExportType = self.ExportMap[Export.ClassIndex.AsExport].SuperIndex.Resource.ObjectName
            elif Export.ClassIndex.IsImport:
                ExportType = self.ImportMap[Export.ClassIndex.AsImport].ObjectName
            else:
                raise ParserException("failed to get export type")
            Export.name = ExportType

            self.reader.seek(Export.SerialOffset - self.PackageFileSummary.TotalHeaderSize, 0)

            self.reader.bulk_offset = Export.SerialSize + self.PackageFileSummary.TotalHeaderSize  # ?

            pos = self.reader.base_stream.tell()
            ExportData = Registry().get_export_reader(ExportType.string, Export, self.reader)
            try:
                ExportData.deserialize(pos + Export.SerialSize)
            except Exception as e:
                raise e
                logger.error(f"Could not read {ExportType.string} correctly")
            Export.exportObject = ExportData

            # export event
            trigger = provider.Triggers.get(ExportType.string, False)
            if trigger:
                trigger(ExportData)

            position = self.reader.base_stream.tell()
            if position != pos + Export.SerialSize:
                logger.debug(
                    f"Didn't read ExportType {ExportType.string} properly, at {position}, should be: {pos + Export.SerialSize} behind: {pos + Export.SerialSize - position}")

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

    def get_summary(self) -> FPackageFileSummary:
        return self.PackageFileSummary

    def find_export(self, export_name: str) -> Optional[FObjectExport]:
        for export in self.ExportMap:
            if export_name == export.name.string:
                return export
        return None

    def findObject(self, index: FPackageIndex) -> Optional[Union[FObjectExport, FObjectImport]]:
        if index.IsNull:
            return None
        elif index.IsImport:
            return self.ImportMap[index.AsImport]
        else:
            export = self.ExportMap[index.AsExport]
            return export


class IoPackageReader(Package):
    GlobalData: FIoGlobalData
    Summary: FPackageSummary
    NameMap: Tuple[FNameEntrySerialized]
    ImportMap: Tuple[FPackageObjectIndex]
    ExportMap: Tuple[FExportMapEntry]
    ExportBundle: FExportBundle
    GraphData: Tuple[FImportedPackage]
    ImportedPackages: Tuple['IoPackageReader']

    def __init__(self, uasset: BinaryStream, ubulk: BinaryStream, uptnl: BinaryStream, provider: "Provider",
                 onlyInfo: bool = False):
        reader = uasset
        reader.ubulk_stream = ubulk or uptnl
        reader.game = provider.GameInfo.UEVersion
        reader.PackageReader = self
        self.reader = reader
        self.Provider = provider

        self.Summary = FPackageSummary(reader=reader)

        self.NameMap = ()

        nameHashes = []
        if self.Summary.NameMapNamesSize > 0:
            reader.seek(self.Summary.NameMapNamesOffset, 0)
            nameMapReader = BinaryStream(reader.readBytes(self.Summary.NameMapNamesSize))

            reader.seek(self.Summary.NameMapHashesOffset, 0)
            nameHashReader = BinaryStream(reader.readBytes(self.Summary.NameMapHashesSize))

            FNameEntrySerialized.LoadNameBatch(self.NameMap, nameHashes, nameMapReader, nameHashReader)
            del nameHashReader
            del nameMapReader

        self.ImportMap = ()
        reader.seek(self.Summary.ImportMapOffset, 0)
        import_map_Count = int(
            (self.Summary.ExportMapOffset - self.Summary.ImportMapOffset) / 8)  # size of FPackageObjectIndex
        self.ImportMap = tuple(FPackageObjectIndex(reader) for _ in range(import_map_Count))

        self.ExportMap = ()
        reader.seek(self.Summary.ExportMapOffset, 0)
        exportMapCount = int((self.Summary.ExportBundlesOffset - self.Summary.ExportMapOffset) / FExportMapEntry.SIZE)
        self.ExportMap = tuple(FExportMapEntry(reader) for _ in range(exportMapCount))

        reader.seek(self.Summary.ExportBundlesOffset, 0)
        self.ExportBundle = FExportBundle(reader)

        if onlyInfo:
            return
        reader.seek(self.Summary.GraphDataOffset, 0)
        self.GraphData = reader.readTArray(FImportedPackage, reader)
        self.ImportedPackages = tuple(
            provider.get_package(iD.index).parse_package(onlyInfo=True) for iD in self.GraphData)

        allExportDataOffset = self.Summary.GraphDataOffset + self.Summary.GraphDataSize
        currentExportDataOffset = allExportDataOffset

        for i in range(self.ExportBundle.Header.EntryCount):
            export_entry = self.ExportBundle.Entries[self.ExportBundle.Header.FirstEntryIndex + i]
            if export_entry.CommandType == EExportCommandType.ExportCommandType_Serialize:
                Export = self.ExportMap[export_entry.LocalExportIndex]  # self.ExportMap[i]

                self.reader.seek(currentExportDataOffset, 0)

                ExportName = resolveObjectIndex(self, provider.GlobalData, index=Export.ClassIndex).getName()
                ExportData = Registry().get_export_reader(ExportName.string, Export, self.reader)
                ExportData.deserialize(currentExportDataOffset + Export.CookedSerialSize)
                Export.name = ExportName
                Export.exportObject = ExportData

                position = self.reader.base_stream.tell()
                if position != currentExportDataOffset + Export.CookedSerialSize:
                    logger.debug(
                        f"Didn't read ExportType {ExportName.string} properly, at {position}, should be: {currentExportDataOffset + Export.CookedSerialSize} behind: {currentExportDataOffset + Export.CookedSerialSize - position}")
                currentExportDataOffset += Export.CookedSerialSize
