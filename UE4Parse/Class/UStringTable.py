from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Objects.FName import FName
from UE4Parse.Objects.FStringTable import FStringTable


class UStringTable(UObject):
    StringTable: FStringTable
    StringTableId = FName

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)
        reader.seek(4)  # idk why

        self.StringTable = FStringTable(reader)
        self.StringTableId = reader.readFName()

        self.Dict["StringTable"] = self.StringTable
        self.Dict["StringTableId"] = self.StringTableId
