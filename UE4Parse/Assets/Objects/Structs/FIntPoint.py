from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream


class FIntPoint(StructInterface):
    position: int
    X: int
    Y: int

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        self.X = reader.readInt32()
        self.Y = reader.readInt32()

    @classmethod
    def default(cls):
        cls = cls.__new__(cls)
        cls.position = -1
        cls.X, cls.Y = (0,0,)
        return cls

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y
        }
