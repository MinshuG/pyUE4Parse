from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Objects.Meshes.FStaticMeshLODResources import FStaticMeshLODResources

MAX_STATIC_UV_SETS_UE4 = 8
MAX_STATIC_LODS_UE4 = 8


class UStaticMesh:
    StripData: FStripDataFlags
    BodySetup: UObject = None  # UBodySetup
    NavCollision: UObject = None  # UNavCollision
    LightingGuid: FGuid
    Sockets: List[UObject]
    LODs: List[FStaticMeshLODResources]
    Bounds: FBoxSphereBounds
    LODsShareStaticLighting = False
    ScreenSize: list
    StaticMaterials: List[FStaticMaterial] = []
    Materials: List[UMaterialInterface] = []

    def __init__(self, reader: BinaryStream):
        pass
