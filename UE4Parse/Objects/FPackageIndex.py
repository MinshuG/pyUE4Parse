from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UE4Parse.BinaryReader import BinaryStream


class FPackageIndex:
    Index: int
    # Reader: BinaryStream
    IsNull: bool
    IsImport: bool
    IsExport: bool
    AsImport: int
    AsExport: int

    def __init__(self, reader: "BinaryStream") -> None:
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
            # return Resource.GetValue() # too much
            return {
                "ObjectName": Resource.ObjectName.string,
                "OuterIndex": Resource.OuterIndex.GetValue()
            }
        return self.Index

    def __str__(self):
        if self.IsExport:
            return f"Export: {self.AsExport}"
        elif self.IsImport:
            return f"Import: {self.AsImport}"
        else:
            return None
