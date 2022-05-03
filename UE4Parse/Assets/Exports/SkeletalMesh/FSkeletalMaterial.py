from typing import Optional, Union
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FObjectExport import FObjectExport
from UE4Parse.Assets.Objects.FObjectImport import FObjectImport
from UE4Parse.Assets.Objects.Meshes.FEditorObjectVersion import FEditorObjectVersion
from UE4Parse.Assets.Objects.Meshes.FMeshUVChannelInfo import FMeshUVChannelInfo
from UE4Parse.Assets.Objects.Meshes.FRenderingObjectVersion import FRenderingObjectVersion
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version
from UE4Parse.Versions.FCoreObjectVersion import FCoreObjectVersion
from UE4Parse.Versions.FRecomputeTangentCustomVersion import FRecomputeTangentCustomVersion


class FSkeletalMaterial:
    Material: Optional[Union[FObjectExport, FObjectImport]]
    MaterialSlotName: FName
    ImportedMaterialSlotName: FName
    UVChannelData: FMeshUVChannelInfo

    def __init__(self, reader: FAssetReader):
        self.Material = reader.readObject()
        self.ImportedMaterialSlotName = FName("None")
        if FEditorObjectVersion().get(reader) >= 10:
            self.MaterialSlotName = reader.readFName()
            b_serialize_imported_material_slot_name = not reader.is_filter_editor_only
            if FCoreObjectVersion().get(reader) >= FCoreObjectVersion.Type.SkeletalMaterialEditorDataStripping:
                b_serialize_imported_material_slot_name = reader.readBool()

            if b_serialize_imported_material_slot_name:
                self.ImportedMaterialSlotName = reader.readFName()
        else:
            if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_MOVE_SKELETALMESH_SHADOWCASTING:
                reader.seek(4, 1)

            if FRecomputeTangentCustomVersion().get(reader) >= FRecomputeTangentCustomVersion.Type.RuntimeRecomputeTangent:
                    reader.seek(4, 1) # bRecomputeTangent
        

        if FRenderingObjectVersion().get(reader) >= FRenderingObjectVersion.TextureStreamingMeshUVChannelData:
            self.UVChannelData = FMeshUVChannelInfo(reader)
        else:
            self.UVChannelData = None

    def GetValue(self):
        return {
            'Material': self.Material.GetValue(),
            'MaterialSlotName': self.MaterialSlotName.GetValue(),
            'ImportedMaterialSlotName': self.ImportedMaterialSlotName.GetValue(),
            'UVChannelData': self.UVChannelData.GetValue() if self.UVChannelData else None
        }
