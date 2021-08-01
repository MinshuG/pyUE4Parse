from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName


class StringTableEntry:
    TableId: FName
    Key: str

    def __init__(self, reader: BinaryStream):
        self.TableId = reader.readFName()
        self.Key = reader.readFString()

    def GetValue(self):
        return {
            "TableId": self.TableId.string,
            "Key": self.Key
        }