from typing import TYPE_CHECKING


from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Versions.FFrameworkObjectVersion import FFrameworkObjectVersion
from UE4Parse.Assets.Exports.UObjects import UObject

if TYPE_CHECKING:
    from UE4Parse.Readers.FAssetReader import FAssetReader


@register_export
class UField(UObject):
    __slots__ = ("Next",)
    Next: FPackageIndex  # Next Field in the linked list

    def __init__(self, reader: 'FAssetReader'):
        super(UField, self).__init__(reader)

    def deserialize(self, validpos):
        super(UField, self).deserialize(validpos)

        if FFrameworkObjectVersion().get(self.reader) < FFrameworkObjectVersion.Type.RemoveUField_Next:
            self.Next = FPackageIndex(self.reader)
        else:
            self.Next = FPackageIndex(0)

    def GetValue(self):
        props = super().GetValue()
        props["Next"] = self.Next.GetValue()
        return props
