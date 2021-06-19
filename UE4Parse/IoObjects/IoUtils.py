from UE4Parse.Objects.FName import FName
from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry
from typing import TYPE_CHECKING
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.IoObjects.FScriptObjectDesc import FScriptObjectDesc

if TYPE_CHECKING:
    from ..PackageReader import IoPackageReader
    from UE4Parse.Class.UObjects import UObject

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
    def __init__(self, pkg: 'IoPackageReader', exportEntry: FExportMapEntry, importedPkg: 'IoPackageReader' = None) -> None:
        self.pkg = pkg
        self.entry = exportEntry
        if importedPkg is None:
            importedPkg = pkg
        self.importedPkg = importedPkg

    def getName(self):
        return FName(str(self.entry.ObjectName))

    def getOuter(self):
        return resolveObjectIndex(self.pkg, self.pkg.Provider.GlobalData, self.entry.OuterIndex)
    
    def getSuper(self):
        return resolveObjectIndex(self.pkg, self.pkg.Provider.GlobalData, self.entry.SuperIndex)

    def getClass(self):
        return resolveObjectIndex(self.pkg, self.pkg.Provider.GlobalData, self.entry.ClassIndex)

    def getObject(self) -> 'UObject':
        return self.entry.exportObject

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
        self.PackageReader = pkg
        self.globaldata = globaldata

    def getName(self):
        return self.scriptobject.Name

    def getOuter(self):
        return resolveObjectIndex(self.PackageReader, self.globaldata, self.scriptobject.OuterIndex)

    def GetValue(self):
        outer = self.getOuter()
        return {
            "Name": self.getName().GetValue(),
            "OuterIndex": outer.GetValue() if outer is not None else None
        }

    def ListResolve(self):
        return self.getName().GetValue()
