from typing import Type
from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FText import FText


class FNavAgentSelectorCustomization(StructInterface):
    SupportedDesc: FText

    def __init__(self, reader: BinaryStream):
        self.SupportedDesc = FText(reader)

    @classmethod
    def default(cls: Type['FNavAgentSelectorCustomization'])->'FNavAgentSelectorCustomization':
        inst = cls.__new__(cls)
        inst.SupportedDesc = FText.default()
        return inst

    def GetValue(self):
        return self.SupportedDesc.GetValue()
