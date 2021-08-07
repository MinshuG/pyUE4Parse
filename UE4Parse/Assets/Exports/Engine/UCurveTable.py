from enum import IntEnum
from typing import Dict
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Versions.FFortniteMainBranchObjectVersion import FFortniteMainBranchObjectVersion


class ECurveTableMode(IntEnum):
    Empty = 0
    SimpleCurves = 1
    RichCurves = 2


@register_export
class UCurveTable(UObject):
    RowMap: Dict[FName, UObject]
    CurveTableMode: ECurveTableMode

    def __init__(self, reader):
        super().__init__(reader)
        self.RowMap = {}

    def deserialize(self, validpos):
        super().deserialize(validpos)

        reader = self.reader
        num_rows = reader.readInt32()

        b_upgrading_ct = FFortniteMainBranchObjectVersion().get(
            reader) < FFortniteMainBranchObjectVersion.Type.ShrinkCurveTableSize

        if b_upgrading_ct:
            self.CurveTableMode = ECurveTableMode.RichCurves if num_rows > 0 else ECurveTableMode.Empty
        else:
            self.CurveTableMode = ECurveTableMode(reader.readByteToInt())

        for i in range(num_rows):
            row_name = reader.readFName()
            obj = UObject(reader, True)
            obj.type = "SimpleCurve" if self.CurveTableMode == ECurveTableMode.SimpleCurves else "RichCurve"
            obj.deserialize(0)
            self.RowMap[row_name] = obj

    def GetValue(self) -> dict:
        props = super(UCurveTable, self).GetValue()
        props["RowMap"] = {key.GetValue(): value.GetValue() for key, value in self.RowMap.items()}
        return props
