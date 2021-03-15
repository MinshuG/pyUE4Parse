from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Objects.Meshes import FStaticMeshVertexBuffer
from UE4Parse.Objects.Meshes.FStaticMeshSection import FStaticMeshSection

CDSF_AdjancencyData: int = 1
CDSF_MinLodData: int = 2
CDSF_ReversedIndexBuffer: int = 4
CDSF_RaytracingResources: int = 8


class FStaticMeshLODResources:
    stripFlags: FStripDataFlags
    sections: List[FStaticMeshSection]
    vertexBuffer = List[FStaticMeshVertexBuffer]
    # positionVertexBuffer: FPositionVertexBuffer
    # colorVertexBuffer: FColorVertexBuffer
    # indexBuffer: FRawStaticIndexBuffer
    # reversedIndexBuffer: FRawStaticIndexBuffer
    # depthOnlyIndexBuffer: FRawStaticIndexBuffer
    # reversedDepthOnlyIndexBuffer: FRawStaticIndexBuffer
    # wireframeIndexBuffer: FRawStaticIndexBuffer
    # adjacencyIndexBuffer: FRawStaticIndexBuffer
    # maxDeviation: float
    # isLODCookedOut = False
    inlined = False

    def __init__(self, reader: BinaryStream):
        pass
