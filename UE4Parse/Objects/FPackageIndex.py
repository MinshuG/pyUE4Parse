from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Globals import Globals

class FPackageIndex:
    Index = None
    Reader = None
    IsNull: bool = None
    IsImport: bool = None
    IsExport: bool = None
    AsImport: int = None
    AsExport: int = None

    def __init__(self, reader: BinaryStream) -> None:

        self.Index = reader.readInt32()
        self.Reader = reader
        self.IsNull = self.Index == 0
        self.IsImport = self.Index < 0
        self.IsExport = self.Index > 0
        self.AsImport = -self.Index - 1
        self.AsExport = self.Index - 1

    @property
    def Resource(self):
        LegacyPackageReader = self.Reader.PackageReader
        if not self.IsNull:  # hmm
            if self.IsImport and self.AsImport < len(LegacyPackageReader.ImportMap):
                return LegacyPackageReader.ImportMap[self.AsImport]

            if self.IsExport and self.AsExport < len(LegacyPackageReader.ExportMap):
                return LegacyPackageReader.ExportMap[self.AsExport]
        return None

    def GetValue(self):
        Resource = self.Resource
        if Resource is not None:
            return {
                "ObjectName": Resource.ObjectName.string,
                "OuterIndex": Resource.OuterIndex.GetValue()
            }
        return self.Index
