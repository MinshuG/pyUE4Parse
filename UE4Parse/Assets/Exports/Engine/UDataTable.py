from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Assets.Objects.FName import FName
from typing import Dict
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Exports.ExportRegistry import register_export


@register_export
class UDataTable(UObject):
    RowMap: Dict[FName, UObject]
    
    def __init__(self, reader):
        super().__init__(reader)
        self.RowMap = {}

    def deserialize(self, validpos):
        super().deserialize(validpos)

        reader = self.reader

        struct_name = self.try_get("RowStruct").Name.string

        num_rows = reader.readInt32()
        for i in range(num_rows):
            name = reader.readFName()
            row = UObject(reader, True)
            row.type = struct_name
            row.deserialize(0)
            self.RowMap[name] = row

    def GetValue(self) -> dict:
        props = super(UDataTable, self).GetValue()
        props["Rows"] = {key.GetValue(): value.GetValue() for key, value in self.RowMap.items()}
        return props

