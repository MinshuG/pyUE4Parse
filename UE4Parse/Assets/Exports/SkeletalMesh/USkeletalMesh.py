from typing import List
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Assets.Exports.SkeletalMesh.FSkeletalMaterial import FSkeletalMaterial
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Assets.Objects.Meshes.FBoxSphereBounds import FBoxSphereBounds


@register_export
class USkeletalMesh(UObject):
    Materials: List[UObject]
    
    def deserialize(self, validpos):
        super().deserialize(validpos)

        strip_data = FStripDataFlags(self.reader)
        self.ImportedBounds = FBoxSphereBounds(self.reader)
        self.Materials  = self.reader.readTArray(lambda:FSkeletalMaterial(self.reader))

    def GetValue(self):
        props = super().GetValue()
        props["ImportedBounds"] = self.ImportedBounds.GetValue()
        props["Materials"] = [m.GetValue() for m in self.Materials]
        return props
