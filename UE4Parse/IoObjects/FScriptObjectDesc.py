from UE4Parse.IoObjects import FScriptObjectEntry
from UE4Parse.IoObjects.FMappedName import FMappedName
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.Assets.Objects.FName import FName


class FScriptObjectDesc:
    Name: FName
    FullName: FName
    GlobalImportIndex: FPackageObjectIndex
    OuterIndex: FPackageObjectIndex
    
    def __init__(self, name, fmappedName: FMappedName, fScriptObjectEntry: FScriptObjectEntry):
        self.Name = FName(name, fmappedName.Index, fmappedName.Number)
        self.GlobalImportIndex = fScriptObjectEntry.GlobalIndex
        self.OuterIndex = fScriptObjectEntry.OuterIndex
