import json


def ToJson(PackageReader, SaveFileName=None, jwp_struct=False):
    NameMaps = None  # PackageReader.NameMap
    ImportMaps = None  # PackageReader.ImportMap
    Exports = PackageReader.DataExports
    ExportTypes = PackageReader.DataExportTypes
    Dict = {}

    if Exports is not None:
        ExportList = []

        for i in range(len(ExportTypes)):
            ExportType = ExportTypes[i].string

            values = {}
            for Export in Exports[i]:
                hmm = Export.GetValue()
                values.update(hmm)
                # ExportList.append(mydict)

            mydict = {
                "ExportType": ExportType,
                "ExportValue": values
            }

            ExportList.append(mydict)

        Dict["Exports"] = ExportList

    if ImportMaps is not None:
        Dict["ImportMap"] = []
        for ImportMap in ImportMaps:
            ImportMap = {
                "ClassName": ImportMap.ClassName.String.Name,
                "ClassPackage": ImportMap.ClassPackage.String.Name,
                "ObjectName": ImportMap.ObjectName.String.Name
            }
            Dict["ImportMap"].append(ImportMap)

    if NameMaps is not None:
        Dict["NameMap"] = []
        for NameMap in NameMaps:
            Dict["NameMap"].append(NameMap.Name)

    if SaveFileName is not None:
        with open(SaveFileName, "w") as f:
            json.dump(Dict, f, indent=4)
    return Dict
