from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Versions.EUEVersion import Versions, GAME_UE4
from UE4Parse.Assets.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Assets.Exports.StaticMesh.FStaticMeshUVItem import FStaticMeshUVItem


class FStaticMeshVertexBuffer:
    NumTexCoords: int
    Strides: int
    NumVertices: int
    UseFullPrecisionUVs: bool
    UseHighPrecisionTangentBasis: bool
    UV: List[FStaticMeshUVItem]

    def __init__(self, reader: BinaryStream):
        StripFlags = FStripDataFlags(reader, Versions.VER_UE4_STATIC_SKELETAL_MESH_SERIALIZATION_FIX)
        self.NumTexCoords = reader.readInt32()
        self.Strides = reader.readInt32() if reader.game < GAME_UE4(19) else -1

        self.NumVertices = reader.readInt32()
        self.UseFullPrecisionUVs = reader.readBool()
        self.UseHighPrecisionTangentBasis = reader.readBool() if reader.game >= GAME_UE4(12) else False

        if not StripFlags.isDataStrippedForServer():
            if reader.game < GAME_UE4(19):
                self.UV = reader.readTArray_W_Arg(FStaticMeshUVItem().read, reader, self.UseHighPrecisionTangentBasis,
                                                  self.NumTexCoords, self.UseFullPrecisionUVs)
            else:
                # reader.readBulkTArray()
                itemSize = reader.readInt32()
                itemCount = reader.readInt32()

                if itemCount != self.NumVertices:
                    raise ParserException(f"{itemCount=} != {self.NumVertices=}")

                pos = reader.tell()
                self.UV = [FStaticMeshUVItem().construct(
                    FStaticMeshUVItem().serialize_tangents(reader, self.UseHighPrecisionTangentBasis), []) for _ in range(self.NumVertices)]

                if reader.tell() - pos != itemSize * itemCount:
                    raise ParserException(
                        f"Read incorrect amount of tangent bytes, at {reader.tell()}, should be: {pos + itemSize * itemCount} behind: {pos + (itemSize * itemCount) - pos}")

                itemSize = reader.readInt32()
                itemCount = reader.readInt32()
                if itemCount != self.NumVertices * self.NumTexCoords:
                    raise ParserException(f"{itemCount=} != NumVertices * NumTexCoords = {self.NumVertices * self.NumTexCoords}")

                pos = reader.tell()
                for i in range(self.NumVertices):
                    self.UV[i].UV = FStaticMeshUVItem().serialize_texcoords(reader, self.NumTexCoords, self.UseFullPrecisionUVs)

                if reader.tell() - pos != itemSize * itemCount:
                    raise ParserException(
                        f"Read incorrect amount of Texture Coordinate bytes, at {reader.tell()}, should be: {pos + itemSize * itemCount} behind: {pos + (itemSize * itemCount) - pos}")
        else:
            self.UV = []

    def GetValue(self):
        return {
            "NumTexCoords": self.NumTexCoords,
            "Strides": self.Strides,
            "NumVertices": self.NumVertices,
            "UseFullPrecisionUVs": self.UseFullPrecisionUVs,
            "UseHighPrecisionTangentBasis": self.UseHighPrecisionTangentBasis,
            "UV": [x.GetValue() for x in self.UV]
        }
