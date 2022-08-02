from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream


class FColor(StructInterface):
    position: int
    R: int
    G: int
    B: int
    A: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.R = reader.readByteToInt()
        self.G = reader.readByteToInt()
        self.B = reader.readByteToInt()
        self.A = reader.readByteToInt()

    @classmethod
    def default(cls):
        cls = cls.__new__(cls)
        cls.position = -1
        cls.R, cls.G, cls.B, cls.A = (0,0,0,0,)
        return cls

    def GetValue(self):
        return {
            "R": self.R,
            "G": self.G,
            "B": self.B,
            "A": self.A
        }


class FLinearColor(StructInterface):
    position: int
    R: float
    G: float
    B: float
    A: float

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.R = reader.readFloat()
        self.G = reader.readFloat()
        self.B = reader.readFloat()
        self.A = reader.readFloat()

    @classmethod
    def default(cls):
        cls = cls.__new__(cls)
        cls.position = -1
        cls.R, cls.G, cls.B, cls.A = (0.0,0.0,0.0,0.0,)
        return cls

    def GetValue(self):
        return {
            "R": self.R,
            "G": self.G,
            "B": self.B,
            "A": self.A
        }
