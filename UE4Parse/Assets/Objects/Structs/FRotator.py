from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream


class FRotator(StructInterface):
    SIZE = 4+4+4
    position: int
    Pitch: float
    Yaw: float
    Roll: float

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Pitch = reader.readFloat()
        self.Yaw = reader.readFloat()
        self.Roll = reader.readFloat()
    
    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.Pitch = 0.0
        inst.Yaw = 0.0
        inst.Roll = 0.0
        return inst

    def GetValue(self):
        return {
            "Pitch": self.Pitch,
            "Yaw": self.Yaw,
            "Roll": self.Roll
        }
