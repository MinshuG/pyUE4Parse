from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FStringTable import FStringTable


@register_export
class UStringTable(UObject):
    StringTable: FStringTable
    StringTableId = FName

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)
    
    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader
        self.StringTable = FStringTable(reader)
        self.StringTableId = reader.readFName()

    def GetValue(self) -> dict:
        return {
            "StringTable": self.StringTable.GetValue(),
            "StringTableId": self.StringTableId.GetValue()
        }
        # self.Dict["StringTable"] = self.StringTable
        # self.Dict["StringTableId"] = self.StringTableId
