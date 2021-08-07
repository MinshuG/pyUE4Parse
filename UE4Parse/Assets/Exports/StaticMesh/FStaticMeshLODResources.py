from typing import List, Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import GAME_UE4
from UE4Parse.Assets.Objects.FByteBulkData import FByteBulkData
from UE4Parse.Assets.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Assets.Objects.Meshes.FColorVertexBuffer import FColorVertexBuffer
from UE4Parse.Assets.Exports.StaticMesh.FPositionVertexBuffer import FPositionVertexBuffer
from UE4Parse.Assets.Exports.StaticMesh.FRawStaticIndexBuffer import FRawStaticIndexBuffer
from UE4Parse.Assets.Exports.StaticMesh.FStaticMeshSection import FStaticMeshSection
from UE4Parse.Assets.Exports.StaticMesh.FStaticMeshVertexBuffer import FStaticMeshVertexBuffer
from UE4Parse.Assets.Objects.Meshes.FWeightedRandomSampler import FWeightedRandomSampler

CDSF_AdjancencyData: int = 1
CDSF_MinLodData: int = 2
CDSF_ReversedIndexBuffer: int = 4
CDSF_RaytracingResources: int = 8


class FStaticMeshLODResources:
    stripFlags: FStripDataFlags
    sections: List[FStaticMeshSection]
    vertexBuffer: Optional[FStaticMeshVertexBuffer] = None
    positionVertexBuffer: Optional[FPositionVertexBuffer] = None
    colorVertexBuffer: Optional[FColorVertexBuffer] = None
    indexBuffer: Optional[FRawStaticIndexBuffer] = None
    reversedIndexBuffer: Optional[FRawStaticIndexBuffer] = None
    depthOnlyIndexBuffer: Optional[FRawStaticIndexBuffer] = None
    reversedDepthOnlyIndexBuffer: Optional[FRawStaticIndexBuffer] = None
    wireframeIndexBuffer: Optional[FRawStaticIndexBuffer] = None
    adjacencyIndexBuffer: Optional[FRawStaticIndexBuffer] = None
    maxDeviation: float
    is_lod_cooked_out = False
    inlined = False

    def __init__(self, reader: BinaryStream):
        self.stripFlags = FStripDataFlags(reader)
        self.sections = reader.readTArray(FStaticMeshSection, reader)
        self.maxDeviation = reader.readFloat()

        if reader.game < GAME_UE4(23):
            if not self.stripFlags.isDataStrippedForServer() and not self.stripFlags.isClassDataStripped(
                    CDSF_MinLodData):
                self.serializeBuffer_legacy(reader)
            return

        self.is_lod_cooked_out = reader.readBool()
        self.inlined = reader.readBool()

        if not self.stripFlags.isDataStrippedForServer() and not self.is_lod_cooked_out:
            if self.inlined:
                self.serializeBuffer(reader)
            else:
                bulk: FByteBulkData = FByteBulkData(reader, ubulk=reader.ubulk_stream,
                                                    bulkOffset=reader.PackageReader.get_summary().BulkDataStartOffset)
                if bulk.Header.ElementCount > 0:  # and bulk.Data is not None:
                    tr = BinaryStream(bulk.Data)
                    tr.game = reader.game
                    tr.version = reader.version
                    self.serializeBuffer(tr)
                else:
                    return  # ??
                reader.readUInt32()  # DepthOnlyNumTriangles
                reader.readUInt32()  # PackedData
                reader.seek(4 * 4 + 2 * 4 + 2 * 4 + 6 * (2 * 4), 1)
                """
                            StaticMeshVertexBuffer = 2x int32, 2x bool
                            PositionVertexBuffer = 2x int32
                            ColorVertexBuffer = 2x int32
                            IndexBuffer = int32 + bool
                            ReversedIndexBuffer
                            DepthOnlyIndexBuffer
                            ReversedDepthOnlyIndexBuffer
                            WireframeIndexBuffer
                            AdjacencyIndexBuffer
                """
        # FStaticMeshBuffersSize
        reader.readUInt32()  # SerializedBuffersSize
        reader.readUInt32()  # DepthOnlyIBSize
        reader.readUInt32()  # ReversedIBsSize

    def serializeBuffer_legacy(self, reader: BinaryStream):
        raise NotImplementedError("UE 4.23+ meshes only currently")
        # self.positionVertexBuffer = FPositionVertexBuffer(reader)
        # self.vertexBuffer = FStaticMeshVertexBuffer(reader)

    def serializeBuffer(self, reader: BinaryStream):
        stripFlags = FStripDataFlags(reader)

        self.positionVertexBuffer = FPositionVertexBuffer(reader)
        self.vertexBuffer = FStaticMeshVertexBuffer(reader)
        self.colorVertexBuffer = FColorVertexBuffer(reader)
        self.indexBuffer = FRawStaticIndexBuffer(reader)

        if not stripFlags.isClassDataStripped(CDSF_ReversedIndexBuffer):
            self.reversedIndexBuffer = FRawStaticIndexBuffer(reader)

        self.depthOnlyIndexBuffer = FRawStaticIndexBuffer(reader)

        if not stripFlags.isClassDataStripped(CDSF_ReversedIndexBuffer):
            self.reversedDepthOnlyIndexBuffer = FRawStaticIndexBuffer(reader)

        if not stripFlags.isEditorDataStripped():
            self.wireframeIndexBuffer = FRawStaticIndexBuffer(reader)

        if not stripFlags.isClassDataStripped(CDSF_AdjancencyData):
            self.adjacencyIndexBuffer = FRawStaticIndexBuffer(reader)

        # UE 4.25+
        if reader.game >= GAME_UE4(25) and not stripFlags.isClassDataStripped(CDSF_RaytracingResources):
            reader.readBulkTArray(reader.readByte)  # Raw data

        for i in range(len(self.sections)):
            FWeightedRandomSampler(reader)  # FStaticMeshSectionAreaWeightedTriangleSampler
        FWeightedRandomSampler(reader)  # FStaticMeshAreaWeightedSectionSampler

    def GetValue(self):
        # GetValue() if Value is not None
        return {
            "Sections": [x.GetValue() for x in self.sections],
            "PositionVertexBuffer": self.positionVertexBuffer.GetValue() if self.positionVertexBuffer is not None else None,
            "VertexBuffer": self.vertexBuffer.GetValue() if self.vertexBuffer is not None else None,
            "ColorVertexBuffer": self.colorVertexBuffer.GetValue() if self.colorVertexBuffer is not None else None,
            "IndexBuffer": self.indexBuffer.GetValue() if self.indexBuffer is not None else None,
            "ReversedIndexBuffer": self.reversedIndexBuffer.GetValue() if self.reversedIndexBuffer is not None else None,
            "DepthOnlyIndexBuffer": self.depthOnlyIndexBuffer.GetValue() if self.depthOnlyIndexBuffer is not None else None,
            "ReversedDepthOnlyIndexBuffer": self.reversedDepthOnlyIndexBuffer.GetValue() if self.reversedDepthOnlyIndexBuffer is not None else None,
            "WireframeIndexBuffer": self.wireframeIndexBuffer.GetValue() if self.wireframeIndexBuffer is not None else None,
            "AdjacencyIndexBuffer": self.adjacencyIndexBuffer.GetValue() if self.adjacencyIndexBuffer is not None else None,
            "MaxDeviation": self.maxDeviation,
            "IsLODCookedOut": self.is_lod_cooked_out,
            "Inlined": self.inlined,
        }
