from typing import List, Any

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Objects.EUEVersion import Versions, GAME_UE4
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Objects.Meshes.FBoxSphereBounds import FBoxSphereBounds
from UE4Parse.Objects.Meshes.FDistanceFieldVolumeData import FDistanceFieldVolumeData
from UE4Parse.Objects.Meshes.FEditorObjectVersion import FEditorObjectVersion
from UE4Parse.Objects.Meshes.FRenderingObjectVersion import FRenderingObjectVersion
from UE4Parse.Objects.Meshes.FStaticMaterial import FStaticMaterial
from UE4Parse.Objects.Meshes.FStaticMeshLODResources import FStaticMeshLODResources
from UE4Parse.Objects.Structs.FRotator import FRotator
from UE4Parse.Objects.Structs.Vector import FVector

MAX_STATIC_UV_SETS_UE4 = 8
MAX_STATIC_LODS_UE4 = 8


class UStaticMesh(UObject):
    LightingGuid: FGuid
    Sockets: Any

    LODs: List[FStaticMeshLODResources]
    Bounds: FBoxSphereBounds
    LODsShareStaticLighting = False
    ScreenSize: List[float] = []
    StaticMaterials: List[FStaticMaterial] = []
    Materials = []

    def __init__(self, reader: BinaryStream, validpos):
        super().__init__(reader, validpos)
        self.StripData = FStripDataFlags(reader)
        bCooked = reader.readBool()
        self.BodySetup = reader.readObject()

        if reader.version >= Versions.VER_UE4_STATIC_MESH_STORE_NAV_COLLISION:
            self.NavCollision = reader.readObject()

        if not self.StripData.isEditorDataStripped():
            if reader.version < Versions.VER_UE4_DEPRECATED_STATIC_MESH_THUMBNAIL_PROPERTIES_REMOVED:
                FRotator(reader)  # dummyThumbnailAngle
                reader.readFloat()  # dummyThumbnailDistance
            highResSourceMeshName = reader.readString()  # highResSourceMeshName
            highResSourceMeshCRC = reader.readUInt32()  #

        self.LightingGuid = FGuid(reader)

        self.Sockets = reader.readTArray(reader.readObject)

        if not self.StripData.isEditorDataStripped:
            raise ParserException("Mesh with editor data not supported")

        # FStaticMeshRenderData
        if bCooked:
            if not bCooked:  # how possible
                pass  # https://github.com/FabianFG/JFortniteParse/blob/558fb2b96985aad5b90c96c8f28950021cf801a0/src/main/kotlin/me/fungames/jfortniteparse/ue4/assets/exports/UStaticMesh.kt#L59
            # if unversioned MinMobileLODIdx int32
            self.LODs = reader.readTArray_W_Arg(FStaticMeshLODResources, reader)

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
                reader.readTArray_W_Arg(FVector, reader)  # Vertices
                reader.readTArray(reader.readUInt16)  # Indics

        if reader.game >= GAME_UE4(14):
            hasSpeedTreeWind = reader.readBool()
            if hasSpeedTreeWind:
                pass  # ignore
            else:
                if FEditorObjectVersion().get(reader) >= FEditorObjectVersion.RefactorMeshEditorMaterials:
                    # UE4.14+ - "Materials" are deprecated, added StaticMaterials
                    self.StaticMaterials = reader.readTArray_W_Arg(FStaticMaterial, reader)

        if len(self.Materials) == 0 and len(self.StaticMaterials) > 0:
            material: FStaticMaterial
            for material in self.StaticMaterials:
                self.Materials.append(material.MaterialInterface)
