
from UE4Parse.Objects.FName import FName


class FScriptObjectDesc:
    Name: FName
    FullName: FName
    # GlobalImportIndex: FPackageObjectIndex
    # OuterIndex: FPackageObjectIndex
    #
    # def __init__(self, name: FNameEntrySerialized, fmappedName: FMappedName, fScriptObjectEntry: FScriptObjectEntry):
    #     self.Name = FName(name, fmappedName.Index, fmappedName.Number)
