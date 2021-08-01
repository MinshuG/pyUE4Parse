from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects import FUniqueObjectGuid

class FLevelSequenceLegacyObjectReference:
    ObjectId: FUniqueObjectGuid = FUniqueObjectGuid
    ObjectPath = ""
    def __init__(self, reader: BinaryStream) -> None:
        self.ObjectId = FUniqueObjectGuid(reader)
        self.ObjectPath = reader.readFString()