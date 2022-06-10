from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName


class FSmartName(StructInterface):
    position: int
    DisplayName: FName

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.DisplayName = reader.readFName()
    
    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = -1
        inst.DisplayName = FName("None")
        return inst

    def GetValue(self):
        return {
            "DisplayName": self.DisplayName
        }
