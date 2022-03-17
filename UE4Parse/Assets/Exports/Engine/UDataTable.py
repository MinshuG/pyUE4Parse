from typing import Dict

from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Logger import get_logger

logger = get_logger(__name__)


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
            try:
                row.deserialize(0)
            except Exception as e:
                self.RowMap[name] = row
                raise ParserException(f"failed to read value for row '{name.GetValue()}'") from e
            self.RowMap[name] = row

    def GetValue(self) -> dict:
        props = super(UDataTable, self).GetValue()
        props["Rows"] = {key.GetValue(): value.GetValue() for key, value in self.RowMap.items()}
        return props

@register_export
class CompositeDataTable(UDataTable):
    pass