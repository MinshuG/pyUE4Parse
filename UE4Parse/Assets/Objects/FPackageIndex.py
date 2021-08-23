from typing import TYPE_CHECKING

from UE4Parse.Assets.Objects.FName import FName

if TYPE_CHECKING:
    from UE4Parse.BinaryReader import BinaryStream


def do_formatting(obj, index):
    outers = []
    current = obj.getOuter()
    while current:
        outers.append(current.getName().string)
        current = current.getOuter()

    ObjectName = f"{outers[0]}:" if len(outers) > 1 else ""
    ObjectName += f"{obj.getName().string}"
    if class_ := obj.getClass():
        ObjectName += f":{class_.getName().string}"

    if len(outers) <= 0:
        ObjectPath = obj.importedPkg.Summary.SourceName.resolve(obj.importedPkg.NameMap)  # ??
        # ObjectPath = abs(index)
    else:
        ObjectPath = f"{outers[-1]}.{abs(index)-1}"

    return {
        "ObjectName": ObjectName,
        "ObjectPath": ObjectPath
    }


class FPackageIndex:
    Index: int
    reader: 'BinaryStream'
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
    def Name(self) -> FName:  # TODO: Fix this
        if self.Resource:
            return FName(self.GetValue().get("ObjectName"))
        else:
            return FName("None")

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
            resolved = resolveObjectIndex(self.Reader.PackageReader, self.Reader.PackageReader.Provider.GlobalData,
                                          Resource)
            if resolved is None: return None
            # list_ = resolved.ListResolve()
            return do_formatting(resolved, self.Index)
        elif isinstance(Resource, FExportMapEntry):
            from UE4Parse.IoObjects.IoUtils import ResolveExportObject
            resolved = ResolveExportObject(self.Reader.PackageReader, Resource)
            # list_ = resolved.ListResolve()
            return do_formatting(resolved, self.Index)

        if Resource is not None:
            if not hasattr(Resource, "ClassIndex"):  # FObjectImport
                ObjectName = f"{Resource.ObjectName.string}"
            else:
                ObjectName = f"{Resource.ObjectName.string}:{Resource.ClassIndex.Name.string}"
            return {
                "ObjectName": ObjectName,
                "OuterIndex": Resource.OuterIndex.GetValue()
            }
        return self.Index

    # def load(self):
    #     return self.reader.PackageReader.fi

    def __str__(self):
        if self.IsExport:
            return f"Export: {self.AsExport} | {self.Name().string}"
        elif self.IsImport:
            return f"Import: {self.AsImport}"
        else:
            return None
