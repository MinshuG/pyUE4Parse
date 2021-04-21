from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.EUEVersion import Versions, GAME_UE4
from UE4Parse.Objects.FStripDataFlags import FStripDataFlags


class FStaticMeshVertexBuffer:
    StripFlags: FStripDataFlags
    NumTexCoords: int
    Strides: int
    NumVertices: int
    UseFullPrecisionUVs: bool
    UseHighPrecisionTangentBasis: bool

    # UV: List[FStaticMeshUVItem]

    def __init__(self, reader: BinaryStream):
        self.StripFlags = FStripDataFlags(reader, Versions.VER_UE4_STATIC_SKELETAL_MESH_SERIALIZATION_FIX)
        self.NumTexCoords = reader.readInt32()
        self.Strides = reader.readInt32() if reader.game > GAME_UE4(19) else -1

        self.NumVertices = reader.readInt32()
        self.UseFullPrecisionUVs = reader.readBool()
