from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry
from typing import TYPE_CHECKING, Tuple, Union

from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Assets.Objects.FObjectExport import FObjectExport
from UE4Parse.Assets.Objects.FObjectImport import FObjectImport

if TYPE_CHECKING:
    from UE4Parse.Assets.PackageReader import Package

def ToJson(PackageReader: 'Package'):
    # NameMap: List[FNameEntrySerialized] = PackageReader.NameMap
    # ImportMap: List[FObjectImport] = PackageReader.ImportMap
    ExportMap: Tuple[Union[FObjectExport, FExportMapEntry]] = PackageReader.ExportMap
    # Dict = {"Exports": []}
    Exports = []
    # "ImportMap": [], "ExportMap": []
    # for Import in ImportMap:
    #     # if isinstance(Import, FPackageObjectIndex):
    #     #     Import = resolveObjectIndex(PackageReader, PackageReader.Provider.GlobalData, Import)
    #     Dict["ImportMap"].append(Import.GetValue())

    for Export in ExportMap:
        # Dict["Exports"].append({"Type": Export.type.string, "Name": Export.name.string, **Export.exportObject.GetValue()})
        Exports.append({"Type": Export.type.string, "Name": Export.name.string, **(Export.exportObject.GetValue() if hasattr(Export, "exportObject") else {})})
        # Dict["ExportMap"].append(Export.GetValue())

    # if NameMap is not None:
    #     Dict["NameMap"] = []
    #     for Name in NameMap:
    #         Dict["NameMap"].append(Name.GetValue())
    return Exports
    # return Dict
