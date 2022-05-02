from typing import Optional, Union
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FObjectExport import FObjectExport
from UE4Parse.Assets.Objects.FObjectImport import FObjectImport
from UE4Parse.Assets.Objects.Meshes.FMeshUVChannelInfo import FMeshUVChannelInfo
from UE4Parse.Assets.Objects.Meshes.FRenderingObjectVersion import FRenderingObjectVersion


class FStaticMaterial:
    MaterialInterface: Optional[Union[FObjectExport, FObjectImport]]
    MaterialSlotName: FName
    ImportedMaterialSlotName: FName
    UVChannelData: FMeshUVChannelInfo

    def __init__(self, reader: BinaryStream):
        self.MaterialInterface = reader.readObject()
        self.MaterialSlotName = reader.readFName()

        if FRenderingObjectVersion().get(reader) >= FRenderingObjectVersion.TextureStreamingMeshUVChannelData:
            self.UVChannelData = FMeshUVChannelInfo(reader)
        else:
            self.UVChannelData = None

    def GetValue(self):
        return {
            'MaterialInterface': self.MaterialInterface,
            'MaterialSlotName': self.MaterialSlotName,
            'UVChannelData': self.UVChannelData.GetValue() if self.UVChannelData else None
        }
