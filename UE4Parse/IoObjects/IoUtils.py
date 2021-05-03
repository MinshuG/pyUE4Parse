from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.IoObjects.FScriptObjectDesc import FScriptObjectDesc


def resolveObjectIndex(pkg, globaldata: FIoGlobalData, index: FPackageObjectIndex):
    if index.IsScriptImport:
        return ResolveScriptObject(globaldata.ScriptObjectByGlobalId[index.typeAndId], pkg, globaldata)
    elif index.IsExport:
        return pkg.ExportMap[index.AsExport]
    elif index.IsPackageImport:
        raise NotImplementedError("ohboi")
    else:
        raise ParserException("impossoble")


class ResolveScriptObject:
    def __init__(self, scriptObject: FScriptObjectDesc, pkg, globaldata):
        self.scriptobject = scriptObject
        self.PackageReader = pkg
        self.globaldata = globaldata

    def getName(self):
        return self.scriptobject.Name

    def getOuter(self):
        return resolveObjectIndex(self.scriptobject.OuterIndex, self.globaldata, self.PackageReader)

    def GetValue(self):
        return {
            "Name": self.getName().GetValue(),
            "OuterIndex": self.getOuter().GetValue()
        }
