from re import X
from typing import Optional, Dict
from UE4Parse.Assets.Objects.Common import StructInterface

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import EUEVersion


def _read_float(reader: BinaryStream):
    """UE5 Large World Coordinates store vector/rotator components as doubles."""
    return reader.readDouble() if reader.game >= EUEVersion.GAME_UE5_0 else reader.readFloat()


class FVector2D(StructInterface):
    position: int
    X: float
    Y: float

    def __init__(self, reader: Optional[BinaryStream] = None):
        if reader is None:
            self.position = -1
            self.X = 0.0
            self.Y = 0.0
            return
        self.position = reader.base_stream.tell()
        self.X = _read_float(reader)
        self.Y = _read_float(reader)

    def construct(self, X: float, Y: float):
        self.X = X
        self.Y = Y
        return self

    @classmethod
    def default(cls):
        return cls()

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y
        }


class FVector(StructInterface):
    position: int
    X: float
    Y: float
    Z: float

    def __init__(self, reader: Optional[BinaryStream] = None):
        if reader is None:
            self.position = -1
            self.X = 0.0
            self.Y = 0.0
            self.Z = 0.0
            return
        self.position = reader.base_stream.tell()
        self.X = _read_float(reader)
        self.Y = _read_float(reader)
        self.Z = _read_float(reader)

    @classmethod
    def default(cls):
        return cls()

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z
        }


class FVector4(StructInterface):
    position: int
    X: float
    Y: float
    Z: float
    W: float  # 4th dimension guys

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.X = _read_float(reader)
        self.Y = _read_float(reader)
        self.Z = _read_float(reader)
        self.W = _read_float(reader)

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = -1
        inst.X, inst.Y, inst.Z, inst.W = (0.0, 0.0, 0.0, 0.0,)
        return inst

    @classmethod
    def new_method(cls, inst):
        inst.Y = 0.0

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z,
            "W": self.W
        }


class FIntVector(StructInterface):
    X: int
    Y: int
    Z: int

    def __init__(self, reader: BinaryStream):
        self.X = reader.readInt32()
        self.Y = reader.readInt32()
        self.Z = reader.readInt32()
    
    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.X = 0
        inst.Y = 0
        inst.Z = 0
        return inst

    def GetValue(self) -> Dict[str, int]:
        return {
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z
        }
