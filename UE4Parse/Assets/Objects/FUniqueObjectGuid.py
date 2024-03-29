from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FGuid import FGuid


class FUniqueObjectGuid:
    Guid: FGuid

    def __init__(self, reader: BinaryStream) -> None:
        self.Guid = FGuid(reader)
    
    def GetValue(self):
        return self.Guid.GetValue()