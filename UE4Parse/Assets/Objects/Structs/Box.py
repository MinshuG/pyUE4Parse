from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.Structs import Vector


class FBox(StructInterface):
    position: int
    Min: Vector.FVector
    Max: Vector.FVector
    bIsValid: bool

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Min = Vector.FVector(reader)
        self.Max = Vector.FVector(reader)
        self.bIsValid = reader.readByte() != 0

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = -1
        inst.Min, inst.Max, inst.bIsValid = (Vector.FVector.default(), Vector.FVector.default(), False)
        return inst

    def GetValue(self):
        return {
            "Min": self.Min.GetValue(),
            "Max": self.Max.GetValue(),
            "bISValid": self.bIsValid
        }


class FBox2D(StructInterface):
    position: int
    Min: Vector.FVector2D
    Max: Vector.FVector2D
    bIsValid: bool

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Min = Vector.FVector2D(reader)
        self.Max = Vector.FVector2D(reader)
        self.bIsValid = reader.readByte() != 0

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = -1
        inst.Min, inst.Max, inst.bIsValid = (Vector.FVector2D.default(), Vector.FVector2D.default(), False)
        return inst

    def GetValue(self):
        return {
            "Min": self.Min.GetValue(),
            "Max": self.Max.GetValue(),
            "bISValid": self.bIsValid
        }
