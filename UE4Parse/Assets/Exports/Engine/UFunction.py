
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Assets.UObject import UStruct


@register_export
class UFunction(UStruct):
    FunctionFlags: int
    EventGraphFunction: FPackageIndex
    EventGraphCallOffset: FPackageIndex

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader

        self.FunctionFlags = reader.readUInt32()
        self.EventGraphFunction = FPackageIndex(reader)
        self.EventGraphCallOffset = FPackageIndex(reader)

    def GetValue(self):
        props = super().GetValue()
        props["FunctionFlags"] = self.FunctionFlags
        props["EventGraphFunction"] = self.EventGraphFunction.GetValue()
        props["EventGraphCallOffset"] = self.EventGraphCallOffset.GetValue()
        return props

