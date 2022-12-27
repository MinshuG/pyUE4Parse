from UE4Parse.IoObjects.FExportMapEntry import FExportMapEntry
from typing import TYPE_CHECKING, Tuple, Union

from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Assets.Objects.FObjectExport import FObjectExport
from UE4Parse.Assets.Objects.FObjectImport import FObjectImport

if TYPE_CHECKING:
    from UE4Parse.Assets.PackageReader import Package

def ToJson(PackageReader: 'Package'):
    ExportMap: Tuple[Union[FObjectExport, FExportMapEntry]] = PackageReader.ExportMap
    Exports = []
    for Export in ExportMap:
        Exports.append({"Type": Export.type.string, "Name": Export.name.string,"Outer": Export.OuterIndex.Name.GetValue() if isinstance(Export, FObjectExport) else "None", **(Export.exportObject.GetValue() if hasattr(Export, "exportObject") else {})})
    return Exports
    # return Dict
