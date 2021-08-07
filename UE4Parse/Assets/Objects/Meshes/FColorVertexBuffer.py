from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import Versions
from UE4Parse.Assets.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Assets.Objects.Structs.Colors import FColor


class FColorVertexBuffer:
    stripFlags: FStripDataFlags
    stride: int
    numVertices: int
    data: List[FColor]

    def __init__(self, reader: BinaryStream):
        self.stripFlags = FStripDataFlags(reader, Versions.VER_UE4_STATIC_SKELETAL_MESH_SERIALIZATION_FIX)
        self.stride = reader.readInt32()
        self.numVertices = reader.readInt32()
        if not self.stripFlags.isDataStrippedForServer() and self.numVertices > 0:
            self.data = reader.readBulkTArray(FColor, reader)
        else:
            self.data = []

    def GetValue(self):
        return {
            "Stride": self.stride,
            "NumVertics": self.numVertices,
            "Data": [x.GetValue() for x in self.data]
        }
