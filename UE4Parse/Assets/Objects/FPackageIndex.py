from typing import TYPE_CHECKING
from functools import singledispatchmethod
from UE4Parse.Assets.Objects.FName import FName

if TYPE_CHECKING:
    from UE4Parse.Readers.FAssetReader import FAssetReader


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
        ObjectPath = obj.importedPkg.Name  # ??
        # ObjectPath = abs(index)
    else:
        ObjectPath = f"{outers[-1]}.{abs(index)-1}"

    return {
        "ObjectName": ObjectName,
        "ObjectPath": ObjectPath
    }


class FPackageIndex:
    Index: int
    reader: 'FAssetReader'
    IsNull: bool
    IsImport: bool
    IsExport: bool
    AsImport: int
    AsExport: int

    @singledispatchmethod
    def __init__(self, reader: "FAssetReader") -> None:
        self.Index = reader.readInt32()
        self.reader = reader

    @__init__.register
    def _(self, v: int):
        self.Index = v
        self.reader = None

    @property
    def IsNull(self): return self.Index == 0
    @property
    def IsImport(self): return self.Index < 0
    @property
    def IsExport(self): return self.Index > 0
    @property
    def AsImport(self): return -self.Index - 1
    @property
    def AsExport(self): return self.Index - 1
    

    @property
    def Name(self) -> FName:  # TODO: Fix this
        if self.Resource:
            return FName(self.GetValue().get("ObjectName"))
        else:
            return FName("None")

    @property
    def Resource(self):
        if not self.IsNull:  # hmm
            PackageReader = self.reader.PackageReader
            if self.IsImport and self.AsImport < len(PackageReader.ImportMap):
                return PackageReader.ImportMap[self.AsImport]

            if self.IsExport and self.AsExport < len(PackageReader.ExportMap):
                return PackageReader.ExportMap[self.AsExport]
        return None

    def GetValue(self):
        Resource = self.Resource
        if Resource is not None:
            from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
            from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry

            if isinstance(Resource, FPackageObjectIndex):
                from UE4Parse.IoObjects.IoUtils import resolveObjectIndex
                resolved = resolveObjectIndex(self.reader.PackageReader, self.reader.PackageReader.Provider.GlobalData,
                                            Resource)
                if resolved is None: return "still this broken?"
                return do_formatting(resolved, self.Index)
            elif isinstance(Resource, FExportMapEntry):
                from UE4Parse.IoObjects.IoUtils import ResolveExportObject
                resolved = ResolveExportObject(self.reader.PackageReader, Resource)
                return do_formatting(resolved, self.Index)

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

    def __repr__(self) -> str:
        return f"<{self.__str__()}>"