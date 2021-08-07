from typing import List, Optional, Tuple

from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Versions.EUEVersion import Versions, GAME_UE4
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Assets.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Assets.Objects.Meshes.FBoxSphereBounds import FBoxSphereBounds
from UE4Parse.Assets.Exports.StaticMesh.FDistanceFieldVolumeData import FDistanceFieldVolumeData
from UE4Parse.Assets.Objects.Meshes.FEditorObjectVersion import FEditorObjectVersion
from UE4Parse.Assets.Objects.Meshes.FRenderingObjectVersion import FRenderingObjectVersion
from UE4Parse.Assets.Exports.StaticMesh.FStaticMaterial import FStaticMaterial
from UE4Parse.Assets.Exports.StaticMesh.FStaticMeshLODResources import FStaticMeshLODResources
from UE4Parse.Assets.Objects.Structs.FRotator import FRotator
from UE4Parse.Assets.Objects.Structs.Vector import FVector
from UE4Parse.Assets.Exports.ExportRegistry import register_export


MAX_STATIC_UV_SETS_UE4 = 8
MAX_STATIC_LODS_UE4 = 8


@register_export
class UStaticMesh(UObject):
    LightingGuid: Optional[FGuid] = None
    Sockets: Tuple[FPackageIndex] = ()
    BodySetup: Optional[FPackageIndex] = None
    NavCollision: Optional[FPackageIndex] = None
    LODs: Tuple[FStaticMeshLODResources] = ()
    Bounds: Optional[FBoxSphereBounds] = None
    LODsShareStaticLighting = False
    ScreenSize: List[float] = []
    StaticMaterials: Tuple[FStaticMaterial] = ()
    Materials = []

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)
    
    def deserialize(self, validpos) -> None:
        super().deserialize(validpos)
        reader = self.reader

        strip_data = FStripDataFlags(reader)
        bCooked = reader.readBool()
        self.BodySetup = FPackageIndex(reader)

        if reader.version >= Versions.VER_UE4_STATIC_MESH_STORE_NAV_COLLISION:
            self.NavCollision = FPackageIndex(reader)

        if not strip_data.isEditorDataStripped():
            if reader.version < Versions.VER_UE4_DEPRECATED_STATIC_MESH_THUMBNAIL_PROPERTIES_REMOVED:
                FRotator(reader)  # dummyThumbnailAngle
                reader.readFloat()  # dummyThumbnailDistance
            highResSourceMeshName = reader.readString()  # highResSourceMeshName
            highResSourceMeshCRC = reader.readUInt32()  #

        self.LightingGuid = FGuid(reader)

        self.Sockets = reader.readTArray(FPackageIndex, reader)

        if not strip_data.isEditorDataStripped:
            raise ParserException("Mesh with editor data not supported")

        # FStaticMeshRenderData
        if bCooked:
            minMobileLODIdx = reader.readInt32() if reader.game >= GAME_UE4(27) else 0

            self.LODs = reader.readTArray(FStaticMeshLODResources, reader) # TODO fix this, but whats broken??

            if reader.game >= GAME_UE4(23):
                NumInlinedLODs = reader.readUInt8()

            if bCooked:
                if reader.version >= Versions.VER_UE4_RENAME_CROUCHMOVESCHARACTERDOWN:
                    isStripped = False
                    if reader.version >= Versions.VER_UE4_RENAME_WIDGET_VISIBILITY:
                        stripflag = FStripDataFlags(reader)
                        isStripped = stripflag.isDataStrippedForServer()
                        if reader.game >= GAME_UE4(21):
                            # 4.21 uses additional strip flag for distance field
                            distanceFieldDataStripFlag = 1
                            isStripped = isStripped | stripflag.isClassDataStripped(distanceFieldDataStripFlag)  # ?
                    if not isStripped:
                        # serialize FDistanceFieldVolumeData for each LOD
                        for _ in range(len(self.LODs) - 1):  # wut why
                            hasDistanceDataField = reader.readBool()
                            if hasDistanceDataField:
                                FDistanceFieldVolumeData(reader)  # VolumeData

            self.Bounds = FBoxSphereBounds(reader)

            if reader.game != GAME_UE4(15):
                self.LODsShareStaticLighting = reader.readBool()

            if reader.game < GAME_UE4(15):
                reader.readBool()  # bReducedBySimplygon

            if FRenderingObjectVersion().get(reader) < FRenderingObjectVersion.TextureStreamingMeshUVChannelData:
                for _ in range(MAX_STATIC_UV_SETS_UE4):  # StreamingTextureFactors
                    reader.readFloat()  # StreamingTextureFactor for each UV set
                reader.readFloat()  # MaxStreamingTextureFactor

            if bCooked:
                maxNumLods = MAX_STATIC_LODS_UE4 if reader.game >= GAME_UE4(9) else 4
                for x in range(maxNumLods):
                    if reader.game >= GAME_UE4(20):
                        reader.readBool()  # bFloatCooked
                    self.ScreenSize.append(reader.readFloat())
        # End of FStaticMeshRenderData

        if bCooked and reader.game >= GAME_UE4(20):
            hasOccluderData = reader.readBool()
            if hasOccluderData:
                reader.readTArray(FVector, reader)  # Vertices
                reader.readTArray(reader.readUInt16)  # Indics

        if reader.game >= GAME_UE4(14):
            hasSpeedTreeWind = reader.readBool()
            if hasSpeedTreeWind:
                pass  # ignore
            else:
                if FEditorObjectVersion().get(reader) >= FEditorObjectVersion.RefactorMeshEditorMaterials:
                    # UE4.14+ - "Materials" are deprecated, added StaticMaterials
                    self.StaticMaterials = reader.readTArray(FStaticMaterial, reader)

        if len(self.Materials) == 0 and len(self.StaticMaterials) > 0:
            material: FStaticMaterial
            for material in self.StaticMaterials:
                self.Materials.append(material.MaterialInterface)

    def GetValue(self) -> dict:
        props = super().GetValue()
        props["Sockets"] = [x.GetValue() for x in self.Sockets]
        props["BodySetup"] = self.BodySetup.GetValue() if self.BodySetup is not None else None
        props["LightingGuid"] = self.LightingGuid.GetValue() if self.LightingGuid is not None else None
        props["LODs"] = [x.GetValue() for x in self.LODs]
        props["Bounds"] = self.Bounds.GetValue() if self.Bounds is not None else None
        props["LODsShareStaticLighting"] = self.LODsShareStaticLighting
        props["NavCollision"] = self.NavCollision.GetValue() if self.NavCollision is not None else None
        props["Materials"] = [x.GetValue() for x in self.Materials]

        return props
