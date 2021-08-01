from typing import Optional, Dict

from UE4Parse.BinaryReader import BinaryStream


class FVector2D:
    position: int
    X: float
    Y: float

    def __init__(self, reader: Optional[BinaryStream] = None):
        if reader is None:
            return
        self.position = reader.base_stream.tell()
        self.X = reader.readFloat()
        self.Y = reader.readFloat()

    def construct(self, X: float, Y: float):
        self.X = X
        self.Y = Y
        return self

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y
        }


class FVector:
    position: int
    X: float
    Y: float
    Z: float

    def __init__(self, reader: Optional[BinaryStream] = None):
        if reader is None:
            return
        self.position = reader.base_stream.tell()
        self.X = reader.readFloat()
        self.Y = reader.readFloat()
        self.Z = reader.readFloat()

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z
        }


class FVector4:
    position: int
    X: float
    Y: float
    Z: float
    W: float  # 4th dimension guys

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.X = reader.readFloat()
        self.Y = reader.readFloat()
        self.Z = reader.readFloat()
        self.W = reader.readFloat()

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z,
            "W": self.W
        }


class FIntVector:
    X: int
    Y: int
    Z: int

    def __init__(self, reader: BinaryStream):
        self.X = reader.readInt32()
        self.Y = reader.readInt32()
        self.Z = reader.readInt32()

    def GetValue(self) -> Dict[str, int]:
        return {
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z
        }
