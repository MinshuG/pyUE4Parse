# from UE4Parse.Class.UStaticMesh import UStaticMesh
from UE4Parse.Class.UTexture2D import UTexture2D
from UE4Parse.Class.UObjects import UObject
from UE4Parse.IoObjects import FIoGlobalData
from UE4Parse.Objects.FName import FName
from UE4Parse.Objects.FObjectExport import FObjectExport
from UE4Parse.Globals import Globals
from UE4Parse.Objects.FObjectImport import FObjectImport
from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Objects.FPackageFileSummary import FPackageFileSummary
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse import ToJson, Logger

logger = Logger.get_logger(__name__)


class LegacyPackageReader:
    NameMap = []
    ImportMap = []
    ExportMap = []
    DataExports = []
    DataExportTypes = []
    PackageFileSummary: FPackageFileSummary

    # @profile
    def __init__(self, uasset: BinaryStream, uexp: BinaryStream = None, ubulk: BinaryStream = None) -> None:
        self.reader = uasset
        self.PackageFileSummary = FPackageFileSummary(self.reader)
        self.NameMap = self.SerializeNameMap()
        self.reader.NameMap = self.NameMap

        self.ImportMap = self.SerializeImportMap()
        self.ExportMap = self.SerializeExportMap()
        self.reader.PackageReader = self

        if uexp is not None:
            self.reader.change_stream(uexp)
        else:
            return

        DataExports = []
        DataExportTypes: list[FName] = []
        for Export in self.ExportMap:
            if Export.ClassIndex.IsNull:
                ExportType = self.reader.readFName()
                DataExportTypes.append(ExportType)
            elif Export.ClassIndex.IsExport:
                ExportType = self.ExportMap[Export.ClassIndex.AsExport].SuperIndex.Resource.ObjectName
                DataExportTypes.append(ExportType)
            elif Export.ClassIndex.IsImport:
                ExportType = self.ImportMap[Export.ClassIndex.AsImport].ObjectName
                DataExportTypes.append(ExportType)
            else:
                raise RuntimeError("failed to get export type")

            data = []
            self.reader.seek(Export.SerialOffset - self.PackageFileSummary.TotalHeaderSize, 0)
            pos = self.reader.base_stream.tell()
            data.append(UObject(self.reader))

            if ExportType.string == "Texture2D":
                Texture = UTexture2D(self.reader, ubulk, Export.SerialSize + self.PackageFileSummary.TotalHeaderSize)
                data.append(Texture)
            # elif ExportType.string == "StaticMesh":
            #      data.append(UStaticMesh(reader=self.reader))
            else:
                pass

            position = self.reader.base_stream.tell()
            if self.reader.base_stream.tell() != pos + Export.SerialSize:
                logger.debug(
                    f"Didn't read ExportType {ExportType.string} properly, at {position}, should be: {pos + Export.SerialSize} behind: {pos + Export.SerialSize - position}")

            DataExports.append(data)

        self.DataExports = DataExports
        self.DataExportTypes: list[FName] = DataExportTypes

    def SerializeNameMap(self):
        if self.PackageFileSummary.NameCount > 0:
            self.reader.seek(self.PackageFileSummary.NameOffset, 0)

            OutNameMap: list[FNameEntrySerialized] = []
            for _ in range(self.PackageFileSummary.NameCount):
                OutNameMap.append(FNameEntrySerialized(self.reader))
            return OutNameMap
        return []

    def SerializeImportMap(self):
        if self.PackageFileSummary.ImportCount > 0:
            self.reader.seek(self.PackageFileSummary.ImportOffset, 0)
            OutImportMap: list[FObjectImport] = []
            for _ in range(self.PackageFileSummary.ImportCount):
                OutImportMap.append(FObjectImport(self.reader))
            return OutImportMap
        return []

    def SerializeExportMap(self):
        if self.PackageFileSummary.ExportCount > 0:
            self.reader.seek(self.PackageFileSummary.ExportOffset, 0)
            OutExportMap: list[FObjectExport] = []
            for _ in range(self.PackageFileSummary.ExportCount):
                OutExportMap.append(FObjectExport(self.reader).read())
            return OutExportMap
        return []

    def get_dict(self, SaveFileName=None, use_jwp_struct=False):
        return ToJson.ToJson(self, SaveFileName, use_jwp_struct)


class IoPackageReader:
    GlobalData: FIoGlobalData

    def __init__(self, uasset: BinaryStream, ubulk: BinaryStream, globalData: FIoGlobalData, onlyInfo: bool = False):
        reader = uasset
