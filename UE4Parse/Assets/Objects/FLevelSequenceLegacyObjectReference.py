from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FUniqueObjectGuid import FUniqueObjectGuid

class FLevelSequenceLegacyObjectReference:
    ObjectId: FUniqueObjectGuid
    ObjectPath = ""

    def __init__(self, reader: BinaryStream) -> None:
        self.ObjectId = FUniqueObjectGuid(reader)
        self.ObjectPath = reader.readFString()
    
    def GetValue(self):
        return {
            "ObjectId": self.ObjectId.GetValue(),
            "ObjectPath": self.ObjectPath
        }