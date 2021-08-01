from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.Structs.Vector import FVector


class FPositionVertexBuffer:
    Verts: List[FVector]
    Stride: int
    NumVertices: int

    def __init__(self, reader: BinaryStream):
        self.Stride = reader.readInt32()
        self.NumVertices = reader.readInt32()
        self.Verts = reader.readBulkTArray(FVector, reader)

    def GetValue(self):
        return {
            "Stride": self.Stride,
            "NumVertices": self.NumVertices,
            "Vertices": [x.GetValue() for x in self.Verts]
        }
