from typing import List

from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Objects.FObjectExport import FObjectExport
from UE4Parse.Objects.FObjectImport import FObjectImport


def ToJson(PackageReader):
    NameMap: List[FNameEntrySerialized] = PackageReader.NameMap
    ImportMap: List[FObjectImport] = PackageReader.ImportMap
    ExportMap: List[FObjectExport] = PackageReader.ExportMap

    Exports = PackageReader.DataExports
    ExportTypes = PackageReader.DataExportTypes
    Dict = {}

    if Exports is not None:
        ExportList = []
        for i in range(len(ExportTypes)):
            ExportType = ExportTypes[i].string
            mydict = {
                "ExportType": ExportType,
                "ExportValue": Exports[i].GetValue()
            }
            ExportList.append(mydict)
        Dict["Exports"] = ExportList

    Dict["ImportMap"] = []
    for Import in ImportMap:
        Dict["ImportMap"].append(Import.GetValue())

    Dict["ExportMap"] = []
    for Export in ExportMap:
        Dict["ExportMap"].append(Export.GetValue())

    if NameMap is not None:
        Dict["NameMap"] = []
        for Name in NameMap:
            Dict["NameMap"].append(Name.GetValue())

    # if SaveFileName is not None:
    #     with open(SaveFileName, "w") as f:
    #         json.dump(Dict, f, indent=4)
    return Dict
