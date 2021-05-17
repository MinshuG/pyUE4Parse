from typing import List

from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Objects.FObjectExport import FObjectExport
from UE4Parse.Objects.FObjectImport import FObjectImport


def ToJson(PackageReader):
    NameMap: List[FNameEntrySerialized] = PackageReader.NameMap
    ImportMap: List[FObjectImport] = PackageReader.ImportMap
    ExportMap: List[FObjectExport] = PackageReader.ExportMap
    Dict = {"Exports": [], "ImportMap": [], "ExportMap": []}

    for Import in ImportMap:
        Dict["ImportMap"].append(Import.GetValue())

    for Export in ExportMap:
        Dict["Exports"].append({"ExportType": Export.name.string, "ExportValue": Export.exportObject.GetValue()})
        Dict["ExportMap"].append(Export.GetValue())

    if NameMap is not None:
        Dict["NameMap"] = []
        for Name in NameMap:
            Dict["NameMap"].append(Name.GetValue())

    return Dict
