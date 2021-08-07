from typing import Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import GAME_UE4
from UE4Parse.Assets.Objects.Structs.Vector import FVector


class FPackedNormal:
    value: int = 0

    def __init__(self, reader: Optional[BinaryStream] = None):
        if reader is None:
            return

        self.value = reader.readUInt32()
        if reader.game >= GAME_UE4(20):
            self.value = self.value ^ 0x80808080

    def to_FVector(self) -> FVector:
        v = FVector(None)
        v.X = (self.value & 0xFF) / 127.5 - 1
        v.Y = ((self.value >> 8) & 0xFF) / 127.5 - 1
        v.Z = ((self.value >> 16) & 0xFF) / 127.5 - 1
        return v

    def from_FVector(self, vector: FVector):
        self.value = int((vector.X + 1) * 127.5) + int((vector.Y + 1) * 127.5) << 8 + int((vector.Z + 1) * 127.5) << 16
        return self

    def GetW(self):
        return (self.value >> 24) / 127.5 - 1

    def GetValue(self):
        return self.value


class FPackedRGBA16N:
    X: int
    Y: int
    Z: int
    W: int

    def __init__(self, reader: BinaryStream):
        self.X = reader.readUInt16()
        self.Y = reader.readUInt16()
        self.Z = reader.readUInt16()
        self.W = reader.readUInt16()

        if reader.game >= GAME_UE4(20):
            self.X = self.X ^ 0x8000
            self.Y = self.Y ^ 0x8000
            self.Z = self.Z ^ 0x8000
            self.W = self.W ^ 0x8000

    def to_packed_normal(self) -> FPackedNormal:
        vector = FVector()
        vector.X = (self.X - 32767.5) / 32767.5
        vector.Y = (self.Y - 32767.5) / 32767.5
        vector.Z = (self.Z - 32767.5) / 32767.5

        return FPackedNormal().from_FVector(vector)
