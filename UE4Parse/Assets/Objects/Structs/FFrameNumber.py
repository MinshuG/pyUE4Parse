from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream


class FFrameNumber(StructInterface):
    position: int   
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readInt32()

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = -1
        inst.Value = 0
        return inst

    def GetValue(self):
        return self.Value
