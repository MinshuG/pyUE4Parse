from typing import Any

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.Meshes.FMeshUVChannelInfo import FMeshUVChannelInfo
from UE4Parse.Assets.Objects.Meshes.FRenderingObjectVersion import FRenderingObjectVersion


class FStaticMaterial:
    MaterialInterface: Any
    MaterialSlotName: FName
    ImportedMaterialSlotName: FName
    UVChannelData: FMeshUVChannelInfo

    def __init__(self, reader: BinaryStream):
        self.MaterialInterface = reader.readObject()
        self.MaterialSlotName = reader.readFName()

        if FRenderingObjectVersion().get(reader) >= FRenderingObjectVersion.TextureStreamingMeshUVChannelData:
            self.UVChannelData = FMeshUVChannelInfo(reader)
