from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry
from typing import TYPE_CHECKING
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.IoObjects.FScriptObjectDesc import FScriptObjectDesc

if TYPE_CHECKING:
    from UE4Parse.Assets.PackageReader import IoPackageReader
    from UE4Parse.Assets.Exports.UObjects import UObject


def resolveObjectIndex(pkg: 'IoPackageReader', globaldata: FIoGlobalData, index: FPackageObjectIndex):
    if index.IsScriptImport:
        return ResolveScriptObject(globaldata.ScriptObjectByGlobalId[index.typeAndId], pkg, globaldata)
    elif index.IsExport:
        return ResolveExportObject(pkg, pkg.ExportMap[index.AsExport], None)
    elif index.IsPackageImport:
        for x in pkg.ImportedPackages:
            for ImportedExport in x.ExportMap:
                if ImportedExport.GlobalImportIndex == index:
                    return ResolveExportObject(pkg, ImportedExport, x)
        return None
    else:
        return None


class ResolveExportObject:
    def __init__(self, pkg: 'IoPackageReader', exportEntry: FExportMapEntry,
                 importedPkg: 'IoPackageReader' = None) -> None:
        self.pkg = pkg
        self.export_map = exportEntry
        if importedPkg is None:
            importedPkg = pkg
        self.importedPkg = importedPkg

    def getName(self):
        return FName(str(self.export_map.ObjectName))

    def getOuter(self):
        return resolveObjectIndex(self.pkg, self.pkg.Provider.GlobalData, self.export_map.OuterIndex)

    def getSuper(self):
        return resolveObjectIndex(self.pkg, self.pkg.Provider.GlobalData, self.export_map.SuperIndex)

    def getClass(self):
        return resolveObjectIndex(self.pkg, self.pkg.Provider.GlobalData, self.export_map.ClassIndex)

    def getObject(self) -> 'UObject':
        return self.export_map.exportObject

    def ListResolve(self):
        resolved = []
        resolved.append(self.getName().string)
        # Dict = {"ObjectName": self.getName().string}
        Class = self.getClass()
        if Class is not None:
            resolved.append(Class.ListResolve())
        outer = self.getOuter()
        if outer is not None:
            # Dict.update({"OuterIndex": outer.GetValue()})
            resolved.append(outer.ListResolve())

        objectpath = self.importedPkg.Summary.SourceName.resolve(self.importedPkg.NameMap)
        resolved.append(objectpath)
        return resolved

    def GetValue(self):
        Dict = {"ObjectName": self.getName().string}
        Class = self.getClass()
        if Class is not None:
            Dict.update({"ClassIndex": Class.GetValue()})
        outer = self.getOuter()
        if outer is not None:
            Dict.update({"OuterIndex": outer.GetValue()})
        return Dict


class ResolveScriptObject:
    def __init__(self, scriptObject: FScriptObjectDesc, pkg, globaldata):
        self.scriptobject = scriptObject
        self.pkg = pkg
        self.globaldata = globaldata

    def getName(self) -> FName:
        return self.scriptobject.Name

    def getClass(self) -> None:  # ??
        return None

    def getOuter(self):
        return resolveObjectIndex(self.pkg, self.globaldata, self.scriptobject.OuterIndex)

    def GetValue(self):
        outer = self.getOuter()
        return {
            "Name": self.getName().GetValue(),
            "OuterIndex": outer.GetValue() if outer is not None else 0
        }

    def ListResolve(self):
        return self.getName().GetValue()
