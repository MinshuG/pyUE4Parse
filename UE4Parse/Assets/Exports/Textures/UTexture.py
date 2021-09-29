from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Assets.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Assets.Exports.UObjects import UObject

# can be ABC?
@register_export
class UTexture(UObject):
    def deserialize(self, validpos):
        super().deserialize(validpos)
        FStripDataFlags(self.reader)
