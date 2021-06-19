from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UE4Parse.BinaryReader import BinaryStream

def doformating(list_):
    if len(list_) == 0: return None
    ObjectName = None
    ObjectPath = None
    if len(list_) >= 1:
        ObjectName = list_[0]
    if len(list_) >= 2:
        ObjectName = ObjectName +":"+list_[1]
    if len(list_) >= 3:
        ObjectPath = list_[2]

    return {
        "ObjectName": ObjectName,
        "ObjectPath": ObjectPath
    }

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
        PackageReader = self.Reader.PackageReader
        if not self.IsNull:  # hmm
            if self.IsImport and self.AsImport < len(PackageReader.ImportMap):
                return PackageReader.ImportMap[self.AsImport]

            if self.IsExport and self.AsExport < len(PackageReader.ExportMap):
                return PackageReader.ExportMap[self.AsExport]
        return None

    def GetValue(self):
        Resource = self.Resource
        from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
        from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry

        if isinstance(Resource, FPackageObjectIndex):
            from UE4Parse.IoObjects.IoUtils import resolveObjectIndex
            resolved = resolveObjectIndex(self.Reader.PackageReader, self.Reader.PackageReader.Provider.GlobalData, Resource)
            if resolved is None: return None
            list_ = resolved.ListResolve()
            return doformating(list_)
        elif isinstance(Resource, FExportMapEntry):
            from UE4Parse.IoObjects.IoUtils import ResolveExportObject
            resolved = ResolveExportObject(self.Reader.PackageReader, Resource)
            list_ = resolved.ListResolve()
            return doformating(list_)

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
