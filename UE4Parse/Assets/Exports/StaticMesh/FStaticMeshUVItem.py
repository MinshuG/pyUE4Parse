from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.Meshes.FMeshUV import FMeshUVFloat, FMeshUVHalf
from UE4Parse.Assets.Objects.Meshes.FPackedNormal import FPackedNormal, FPackedRGBA16N


class FStaticMeshUVItem:
    Normal: List[FPackedNormal]
    UV: List[FMeshUVFloat]

    def read(self, reader: BinaryStream, useHighPrecisionTangents: bool, numStaticUVSets: int, useStaticFloatUVs: bool):
        self.Normal = self.serialize_tangents(reader, useHighPrecisionTangents)
        self.UV = self.serialize_texcoords(reader, numStaticUVSets, useStaticFloatUVs)

    def construct(self, normal, uv):
        self.Normal = normal
        self.UV = uv
        return self

    @staticmethod
    def serialize_tangents(reader: BinaryStream, UseHighPrecisionTangentBasis: bool) -> List[FPackedNormal]:
        if not UseHighPrecisionTangentBasis:
            return [FPackedNormal(reader), FPackedNormal(), FPackedNormal(reader)]  # TangentX and TangentZ
        else:
            normal = FPackedRGBA16N(reader)
            tangent = FPackedRGBA16N(reader)
            return [normal.to_packed_normal(), FPackedNormal(), tangent.to_packed_normal()]

    @staticmethod
    def serialize_texcoords(reader, numStaticUVSets, useStaticFloatUVs) -> List[FMeshUVFloat]:
        if useStaticFloatUVs:
            return [FMeshUVFloat(reader) for _ in range(numStaticUVSets)]
        else:
            return [FMeshUVHalf(reader).to_mesh_uv_float() for _ in range(numStaticUVSets)]

    def GetValue(self):
        return {
            "Normal": [x.GetValue() for x in self.Normal],
            "UV": [x.GetValue() for x in self.UV]
        }
