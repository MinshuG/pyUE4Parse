from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import EUEVersion
from UE4Parse.Assets.Objects.Meshes.FRenderingObjectVersion import FRenderingObjectVersion


class FStaticMeshSection:
    MaterialIndex: int
    FirstIndex: int
    NumTriangles: int
    MinVertexIndex: int
    MaxVertexIndex: int
    EnableCollision: bool
    CastShadow: bool
    ForceOpaque: bool
    VisibleInRayTracing: bool

    def __init__(self, reader: BinaryStream):  # FIXME Something is Broken here
        self.MaterialIndex = reader.readInt32()
        self.FirstIndex = reader.readInt32()
        self.NumTriangles = reader.readInt32()
        self.MinVertexIndex = reader.readInt32()
        self.MaxVertexIndex = reader.readInt32()
        self.EnableCollision = reader.readBool()
        self.CastShadow = reader.readBool()
        self.ForceOpaque = reader.readBool() if FRenderingObjectVersion().get(reader) >= FRenderingObjectVersion.StaticMeshSectionForceOpaqueField else False
        self.VisibleInRayTracing = reader.readBool() if reader.game >= EUEVersion.GAME_UE4_26 else False

    def GetValue(self):
        return {
            "MaterialIndex": self.MaterialIndex,
            "FirstIndex": self.FirstIndex,
            "NumTriangles": self.NumTriangles,
            "MinVertexIndex": self.MinVertexIndex,
            "MaxVertexIndex": self.MaxVertexIndex,
            "EnableCollision": self.EnableCollision,
            "CastShadow": self.CastShadow,
            "ForceOpaque": self.ForceOpaque,
            "VisibleInRayTracing": self.VisibleInRayTracing
        }